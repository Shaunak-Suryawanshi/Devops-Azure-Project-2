import os
import json

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import redis

app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "incident_platform")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_USERNAME = os.getenv("REDIS_USERNAME", "")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")
REDIS_SSL = os.getenv("REDIS_SSL", "false").strip().lower() == "true"
try:
    REDIS_DB = int(os.getenv("REDIS_DB", "0"))
except ValueError:
    REDIS_DB = 0
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "30"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

mongo_client = MongoClient(MONGODB_URI) if MONGODB_URI else None
db = mongo_client[MONGODB_DB_NAME] if mongo_client else None
incidents_collection = db["incidents"] if db is not None else None
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    username=REDIS_USERNAME or None,
    password=REDIS_PASSWORD or None,
    ssl=REDIS_SSL,
    decode_responses=True,
)


def redis_is_available():
    try:
        redis_client.ping()
        return True
    except redis.RedisError:
        return False


def enforce_rate_limit(client_ip):
    if not redis_is_available():
        return None

    key = f"rate_limit:{client_ip}"
    current_count = redis_client.incr(key)
    if current_count == 1:
        redis_client.expire(key, RATE_LIMIT_WINDOW_SECONDS)

    if current_count > RATE_LIMIT_REQUESTS:
        ttl = redis_client.ttl(key)
        return {"error": "rate limit exceeded", "retry_after_seconds": max(ttl, 1)}
    return None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    db_status = "disconnected"
    if mongo_client:
        try:
            mongo_client.admin.command("ping")
            db_status = "connected"
        except PyMongoError:
            db_status = "error"

    redis_status = "connected" if redis_is_available() else "error"

    return {"status": "ok", "service": "incident-platform", "mongodb": db_status, "redis": redis_status}, 200


@app.route("/incidents", methods=["POST"])
def create_incident():
    limit_error = enforce_rate_limit(request.remote_addr or "unknown")
    if limit_error:
        return jsonify(limit_error), 429

    if incidents_collection is None:
        return jsonify({"error": "MongoDB is not configured"}), 500

    payload = request.get_json(silent=True) or {}
    title = (payload.get("title") or "").strip()
    description = (payload.get("description") or "").strip()
    status = (payload.get("status") or "open").strip().lower()

    if not title:
        return jsonify({"error": "title is required"}), 400

    incident = {
        "title": title,
        "description": description,
        "status": status,
    }

    result = incidents_collection.insert_one(incident)
    if redis_is_available():
        redis_client.delete("incidents:all")
    return jsonify({"message": "incident created", "id": str(result.inserted_id)}), 201


@app.route("/incidents", methods=["GET"])
def list_incidents():
    limit_error = enforce_rate_limit(request.remote_addr or "unknown")
    if limit_error:
        return jsonify(limit_error), 429

    if incidents_collection is None:
        return jsonify({"error": "MongoDB is not configured"}), 500

    if redis_is_available():
        cached_incidents = redis_client.get("incidents:all")
        if cached_incidents:
            return jsonify({"source": "cache", "data": json.loads(cached_incidents)}), 200

    incidents = []
    for item in incidents_collection.find().sort("_id", -1):
        incidents.append(
            {
                "id": str(item.get("_id")),
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "status": item.get("status", "open"),
            }
        )
    if redis_is_available():
        redis_client.setex("incidents:all", 60, json.dumps(incidents))
    return jsonify({"source": "database", "data": incidents}), 200


@app.route("/incidents/<title>/status", methods=["PUT"])
def update_incident_status(title):
    limit_error = enforce_rate_limit(request.remote_addr or "unknown")
    if limit_error:
        return jsonify(limit_error), 429

    if incidents_collection is None:
        return jsonify({"error": "MongoDB is not configured"}), 500

    payload = request.get_json(silent=True) or {}
    new_status = (payload.get("status") or "").strip().lower()
    if not new_status:
        return jsonify({"error": "status is required"}), 400

    result = incidents_collection.update_one(
        {"title": title},
        {"$set": {"status": new_status}},
    )

    if result.matched_count == 0:
        return jsonify({"error": "incident not found"}), 404

    if redis_is_available():
        redis_client.delete("incidents:all")
    return jsonify({"message": "incident status updated"}), 200


@app.route("/incidents/search", methods=["GET"])
def search_incidents():
    limit_error = enforce_rate_limit(request.remote_addr or "unknown")
    if limit_error:
        return jsonify(limit_error), 429

    if incidents_collection is None:
        return jsonify({"error": "MongoDB is not configured"}), 500

    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"error": "q query parameter is required"}), 400

    mongo_query = {"title": {"$regex": query, "$options": "i"}}
    incidents = []
    for item in incidents_collection.find(mongo_query):
        incidents.append(
            {
                "id": str(item.get("_id")),
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "status": item.get("status", "open"),
            }
        )
    return jsonify(incidents), 200


@app.route("/session/set", methods=["POST"])
def set_session_value():
    if not redis_is_available():
        return jsonify({"error": "Redis is not available"}), 500

    payload = request.get_json(silent=True) or {}
    user_id = (payload.get("user_id") or "").strip()
    role = (payload.get("role") or "").strip()
    if not user_id or not role:
        return jsonify({"error": "user_id and role are required"}), 400

    redis_client.setex(f"session:{user_id}", 1800, role)
    return jsonify({"message": "session saved", "user_id": user_id}), 200


@app.route("/session/<user_id>", methods=["GET"])
def get_session_value(user_id):
    if not redis_is_available():
        return jsonify({"error": "Redis is not available"}), 500

    role = redis_client.get(f"session:{user_id}")
    if role is None:
        return jsonify({"error": "session not found or expired"}), 404
    return jsonify({"user_id": user_id, "role": role}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1000, debug=True)
