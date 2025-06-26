from flask import Flask, request, jsonify
import pyodbc
import os

app = Flask(__name__)

# Connect to tenant-specific SQL Server database
server = os.getenv('DATABASE_HOST')
database = os.getenv('DATABASE_NAME')
clientID = os.getenv('DATABASE_USER')

conn_str = f'Driver={{ODBC Driver 18 for SQL Server}};Server=tcp:{server},1433;Database={database};UID={clientID};Authentication=ActiveDirectoryMsi;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'

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