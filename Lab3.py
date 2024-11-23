from flask import Flask, request, jsonify, render_template
import psycopg2
from psycopg2 import sql

app = Flask(__name__)


@app.route('/')
def login_page():
    return render_template('index.html')

# Hàm kết nối đến database
def connect_db():
    return psycopg2.connect(
        dbname='thuoc',
        user='postgres',
        password='Tamle90066@',
        host='localhost',
        port='5432'
    )

# API kiểm tra kết nối database
@app.route('/connect', methods=['GET'])
def connect():
    try:
        conn = connect_db()
        conn.close()
        return jsonify({"status": "success", "message": "Kết nối thành công!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# API tải dữ liệu
@app.route('/load_data', methods=['GET'])
def load_data():
    table_name = request.args.get('table', 'thuocuong')
    try:
        conn = connect_db()
        cur = conn.cursor()
        query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name))
        cur.execute(query)
        rows = cur.fetchall()
        conn.close()
        return jsonify({"status": "success", "data": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

# API tìm kiếm
@app.route('/search', methods=['GET'])
def search():
    table_name = request.args.get('table', 'thuocuong')
    ten = request.args.get('ten', '')
    benh = request.args.get('benh', '')
    thuoc = request.args.get('thuoc', '')

    try:
        conn = connect_db()
        cur = conn.cursor()
        search_query = sql.SQL("SELECT * FROM {} WHERE Ten LIKE %s AND Benh LIKE %s AND Thuoc LIKE %s").format(
            sql.Identifier(table_name)
        )
        cur.execute(search_query, ('%' + ten + '%', '%' + benh + '%', '%' + thuoc + '%'))
        rows = cur.fetchall()
        conn.close()
        return jsonify({"status": "success", "data": rows})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
