from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# ---------------- DB ----------------
def init_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            project TEXT,
            qty TEXT,
            status TEXT
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

    if request.method == 'POST':
        project = request.form['project']
        qty = request.form['qty']
        status = request.form['status']

        c.execute(
            "INSERT INTO items (category, project, qty, status) VALUES (?, ?, ?, ?)",
            (category, project, qty, status)
        )
        conn.commit()

    c.execute("SELECT * FROM items WHERE category=?", (category,))
    rows = c.fetchall()
    conn.close()

    return render_template('table.html', category=category, rows=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)