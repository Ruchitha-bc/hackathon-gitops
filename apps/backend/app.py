from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import psycopg2

app = Flask(__name__)
CORS(app)

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


@app.route("/complaints", methods=["POST"])
def add_complaint():

    data = request.get_json()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO complaints(title,description) VALUES(%s,%s) RETURNING id;",
        (data["title"], data["description"])
    )

    ticket_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({
        "status":"Created",
        "id":ticket_id
    }),201


@app.route("/complaints", methods=["GET"])
def get_complaints():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM complaints ORDER BY id DESC;")

    rows = cur.fetchall()

    cur.close()
    conn.close()

    complaints=[]

    for row in rows:
        complaints.append({
            "id":row[0],
            "title":row[1],
            "description":row[2]
        })

    return jsonify(complaints)


if __name__=="__main__":
    init_db()
    app.run(host="0.0.0.0",port=5000)
