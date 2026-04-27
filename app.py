from flask import Flask, render_template, request
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# ---------------- DB ----------------
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            project_number TEXT,
            size TEXT,
            color TEXT,
            quantity TEXT,
            date TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# ---------------- DASHBOARD ----------------
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# ---------------- CATEGORY PAGE ----------------
@app.route('/<category>', methods=['GET', 'POST'])
def category_page(category):

    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    # اضافه کردن دیتا
    if request.method == 'POST':
        project_number = request.form['project_number']
        size = request.form['size']
        color = request.form['color']
        quantity = request.form['quantity']

        date = datetime.now().strftime("%Y-%m-%d")

        c.execute("""
            INSERT INTO items (category, project_number, size, color, quantity, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (category, project_number, size, color, quantity, date))

        conn.commit()

    # گرفتن دیتاها
    c.execute("SELECT * FROM items WHERE category=?", (category,))
    rows = c.fetchall()

    conn.close()

    return render_template('table.html', category=category, rows=rows)


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
