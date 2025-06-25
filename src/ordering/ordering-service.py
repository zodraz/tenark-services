from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Connect to tenant-specific SQL Server database
server = os.getenv('DATABASE_HOST')
database = os.getenv('DATABASE_NAME')
user = os.getenv('DATABASE_USER')
password = os.getenv('DATABASE_PASSWORD')

conn_str = f'Driver={{ODBC Driver 18 for SQL Server}};Server={server},1433;Database={database};UID={user};PWD={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'    

@app.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        quantity = data.get('quantity')
        customer_id = data.get('customer_id')

        if not all([book_id, quantity, customer_id]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Connect to database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Insert order
        query = "INSERT INTO Orders (BookId, Quantity, CustomerId) VALUES (?, ?, ?)"
        cursor.execute(query, (book_id, quantity, customer_id))
        cursor.execute("SELECT SCOPE_IDENTITY() AS Id")
        order_id = cursor.fetchone().Id
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'order_id': int(order_id), 'message': 'Order created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)