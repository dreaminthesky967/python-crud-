from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import pymysql

# ======== DATABASE KONFIGURASI ========
DB_NAME = 'item_name'
DB_USER = 'root'
DB_PASSWORD = ''
DB_HOST = 'localhost'

# ======== CEK DAN BUAT DATABASE JIKA BELUM ADA ========
connection = pymysql.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)
try:
    with connection.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"✅ Database '{DB_NAME}' berhasil dicek/dibuat.")
finally:
    connection.close()

# ======== KONFIGURASI FLASK ========
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#tabel
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)

# inisialisasi daatabase
with app.app_context():
    db.create_all()

def format_rupiah(value):
    return f"Rp {value:,.0f}".replace(",", ".")

app.jinja_env.filters['rupiah'] = format_rupiah

# =routes web itama jinja
@app.route("/")
def index():
    items = Item.query.all()
    msg = request.args.get("msg")
    msg_type = request.args.get("type")
    return render_template("index.html", items=items, msg=msg, msg_type=msg_type)

#api tambah
@app.route("/add", methods=["POST"])
def add_item():
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    
    if not name or not description or not price:
        return redirect(url_for("index", msg="Semua data harus diisi!", type="error"))

    try:
        new_item = Item(name=name, description=description, price=float(price))
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("index", msg="Produk berhasil ditambahkan!", type="success"))
    except ValueError:
        return redirect(url_for("index", msg="Harga harus berupa angka!", type="error"))
#edit
@app.route("/edit/<int:id>", methods=["POST"])
def edit_item(id):
    item = Item.query.get_or_404(id)
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")

    if not name or not description or not price:
        return redirect(url_for("index", msg="Semua data harus diisi!", type="error"))

    try:
        item.name = name
        item.description = description
        item.price = float(price)
        db.session.commit()
        return redirect(url_for("index", msg="Produk berhasil diperbarui!", type="success"))
    except ValueError:
        return redirect(url_for("index", msg="Harga harus berupa angka!", type="error"))
#hapus
@app.route("/delete/<int:id>", methods=["POST"])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("index", msg="Produk berhasil dihapus!", type="success"))

# API Endpoints
@app.route("/api/items", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([{
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "price": item.price
    } for item in items])

@app.route("/api/items/<int:id>", methods=["GET"])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify({
        "id": item.id,
        "name": item.name,
        "description": item.description,
        "price": item.price
    })

@app.route("/api/items", methods=["POST"])
def api_add_item():
    data = request.json
    if not data or "name" not in data or "description" not in data or "price" not in data:
        return jsonify({"error": "Data tidak lengkap"}), 400

    try:
        new_item = Item(name=data["name"], description=data["description"], price=float(data["price"]))
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": "Item berhasil ditambahkan!"}), 201
    except ValueError:
        return jsonify({"error": "Harga harus berupa angka!"}), 400

@app.route("/api/items/<int:id>", methods=["PUT"])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.json
    if not data:
        return jsonify({"error": "Data tidak ditemukan"}), 400

    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)

    try:
        item.price = float(data.get("price", item.price))
    except ValueError:
        return jsonify({"error": "Harga harus berupa angka!"}), 400

    db.session.commit()
    return jsonify({"message": "Item berhasil diperbarui!"})

@app.route("/api/items/<int:id>", methods=["DELETE"])
def delete_api_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item berhasil dihapus!"})

if __name__ == "__main__":
    app.run(debug=True)
