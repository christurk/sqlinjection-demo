from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Create some sample data
    cursor.execute('DELETE FROM users')  # Clear existing data
    sample_users = [
        ('admin', 'admin123', 'admin@example.com', 'admin'),
        ('alice', 'password', 'alice@example.com', 'user'),
        ('bob', 'secret', 'bob@example.com', 'user'),
        ('charlie', 'qwerty', 'charlie@example.com', 'user'),
        ('diana', 'password123', 'diana@example.com', 'user')
    ]
    
    for user in sample_users:
        cursor.execute('INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)', user)
    
    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # VULNERABLE: Direct string concatenation - DON'T DO THIS IN PRODUCTION!
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()
            
            if user:
                # Get all users for admin view
                all_users = []
                if user[4] == 'admin':  # role is at index 4
                    conn = sqlite3.connect('users.db')
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users")
                    all_users = cursor.fetchall()
                    conn.close()
                
                return render_template('dashboard.html', 
                                     user={'username': user[1], 'email': user[3], 'role': user[4]},
                                     all_users=all_users)
            else:
                return render_template('login.html', error="Invalid username or password")
                
        except sqlite3.Error as e:
            return render_template('login.html', error=f"Database error: {str(e)}")
    
    return render_template('login.html')

@app.route('/search')
def search():
    search_query = request.args.get('q', '')
    
    if not search_query:
        return redirect(url_for('login'))
    
    # VULNERABLE: Direct string concatenation - DON'T DO THIS IN PRODUCTION!
    sql_query = f"SELECT * FROM users WHERE username LIKE '%{search_query}%'"
    
    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute(sql_query)
        results = cursor.fetchall()
        conn.close()
        
        return render_template('search.html', 
                             search_query=search_query,
                             sql_query=sql_query,
                             results=results)
        
    except sqlite3.Error as e:
        return render_template('search.html', 
                             search_query=search_query,
                             sql_query=sql_query,
                             error=str(e))

if __name__ == '__main__':
    
    # Initialize database with sample data
    init_db()
    
    print("Available at: http://localhost:5000")
    print("\nSample users:")
    print("- admin / admin123")
    print("- alice / password")
    print("- bob / secret")
    print("\nTry SQL injection payloads:")
    print("- admin'--")
    print("- ' OR '1'='1' --")
    print("- ' UNION SELECT null,version(),null,null,null --")
    
    app.run(debug=True, host='0.0.0.0', port=5000)