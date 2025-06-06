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

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        genre = request.args.get('genre', 'fiction')

        # Connect to database
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Query top 3 books by stock in the genre
        query = "SELECT TOP 3 Id, Title FROM Books WHERE Genre = ? ORDER BY Stock DESC"
        cursor.execute(query, (genre,))
        recommendations = [{'id': row.Id, 'title': row.Title} for row in cursor.fetchall()]

        cursor.close()
        conn.close()

        return jsonify({'recommendations': recommendations}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)