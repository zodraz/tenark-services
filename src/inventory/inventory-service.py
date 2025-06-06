from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Connect to tenant-specific SQL Server database
conn_str = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('DATABASE_HOST', '')};"
    f"DATABASE={os.getenv('DATABASE_NAME', '')};"
    f"UID={os.getenv('DATABASE_USER', 'sa')};"
    f"PWD={os.getenv('DATABASE_PASSWORD', 'Password123')}"
)

@app.route('/inventory', methods=['POST'])
def update_inventory():
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        quantity = data.get('quantity')

        if not all([book_id, quantity]):
            return jsonify({'error': 'Missing required fields'}), 400

        # Connect to database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Update or insert inventory
        query = """
        MERGE INTO Inventory AS target
        USING (SELECT ? AS BookId, ? AS Quantity) AS source
        ON target.BookId = source.BookId
        WHEN MATCHED THEN
            UPDATE SET Quantity = target.Quantity + source.Quantity
        WHEN NOT MATCHED THEN
            INSERT (BookId, Quantity)
            VALUES (source.BookId, source.Quantity);
        """
        cursor.execute(query, (book_id, quantity))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({'book_id': book_id, 'message': 'Inventory updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)