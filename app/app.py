from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
import sqlite3


app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('posts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/events/")
def events():
    conn = get_db_connection()
    usernames = conn.execute('SELECT username FROM posts').fetchall()
    usernames = [u[0] for u in usernames]
    captions = conn.execute('SELECT caption FROM posts').fetchall()
    captions = [c[0] for c in captions]
    imgs = conn.execute('SELECT img FROM posts').fetchall()
    imgs = [i[0] for i in imgs]
    conn.close()
    return render_template('events.html', l = len(usernames), usernames=usernames, captions=captions, imgs=imgs)