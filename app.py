import os
from flask import Flask, request, jsonify, render_template
from flaskext.mysql import MySQL
from flask_cors import CORS


from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
mysql = MySQL()
mysql.init_app(app)

# Database Config
app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST')

# FIX: Added the missing route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_vehicle', methods=["POST"])
def add_vehicle():
    # FIX: Corrected .get_jason() to .get_json()
    data = request.get_json()
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO vehicles (name, category, year, price) VALUES (%s, %s, %s, %s)",
                (data['name'], data['category'], data['year'], data['price']))

    conn.commit()
    return jsonify({"status": "Success"})

@app.route('/get_vehicles', methods=['GET'])
def get_vehicles():
    conn = mysql.connect()
    cursor = conn.cursor()
    # FIX: Corrected FORM to FROM
    cursor.execute("SELECT * FROM vehicles")
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/delete_vehicles/<int:id>', methods=['DELETE'])
def delete_vehicles(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM vehicles WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    return jsonify({"message": "Deleted successfully"})

if __name__== '__main__':
    app.run(debug=True)