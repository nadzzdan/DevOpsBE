from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)

# Database config from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route("/messages", methods=["POST"])
def add_message():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "Message is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (content) VALUES (%s)", (message,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"status": "Message stored"}), 201

@app.route("/messages", methods=["GET"])
def get_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, content FROM messages ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify([{"id": r[0], "content": r[1]} for r in rows])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
