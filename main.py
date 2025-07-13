from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
import os
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class User(BaseModel):
    id: int
    name: str

@app.get("/users")
def get_users():
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password"),
        database=os.getenv("DB_NAME", "testdb")
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return [{"id": r[0], "name": r[1]} for r in result]
