import os
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_db_connection():
    socket_path = os.path.expanduser('~/.local/mariadb/data/mariadb.sock')
    return pymysql.connect(
        user='atharvmscds',
        unix_socket=socket_path,
        db='app',
        cursorclass=pymysql.cursors.DictCursor
    )

# READ: Render table with selected columns
@app.route('/')
def index():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT `Account Id`, `Lead Owner`, `First Name`, `Last Name`, 
                   `Company`, `Phone 1`, `Phone 2`, `Email 1` 
            FROM Leads
        """)
        leads = cursor.fetchall()
    conn.close()
    return render_template('index.html', leads=leads)

# UPDATE: Modify First Name and Last Name
@app.route('/edit/<account_id>', methods=['POST'])
def edit_lead(account_id):
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE Leads 
            SET `First Name` = %s, `Last Name` = %s 
            WHERE `Account Id` = %s
        """, (first_name, last_name, account_id))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

# DELETE: Remove lead from database
@app.route('/delete/<account_id>', methods=['POST'])
def delete_lead(account_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM Leads WHERE `Account Id` = %s", (account_id,))
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)