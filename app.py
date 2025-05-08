from flask import Flask, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)
def get_db_connection():
    """
    Izveido un atgriež savienojumu ar SQLite datubāzi.
    """
    # Atrod ceļu uz datubāzes failu (tas atrodas tajā pašā mapē, kur šis fails)
    db = Path(__file__).parent / "miniVeikals.db"
    # Izveido savienojumu ar SQLite datubāzi
    conn = sqlite3.connect(db)
    # Nodrošina, ka rezultāti būs pieejami kā vārdnīcas (piemēram: product["name"])
    conn.row_factory = sqlite3.Row
    # Atgriež savienojumu
    return conn

@app.route("/")
def index():
    return render_template("index.html")

# Maršruts, kas atbild uz pieprasījumu, piemēram: /produkti/3
# Šeit <int:product_id> nozīmē, ka URL daļā gaidāms produkta ID kā skaitlis
@app.route("/produkti/<int:product_id>")
def products_show(product_id):
    conn = get_db_connection()
    product = conn.execute(
        """
        SELECT products.*,
                taisitajs.name AS taisitajs_nosaukums,
                krasa.name AS krasa_nosaukums,
                materiali.name AS materiali_nosaukums   -- Šeit ir "materiali"
        FROM products
        LEFT JOIN taisitajs ON products.taisitajs = taisitajs.id
        LEFT JOIN krasa ON products.krasa = krasa.id
        LEFT JOIN materiali ON products.material = materiali.id   -- Un šeit
        WHERE products.id = ?
        """,
        (product_id,)
    ).fetchone()
    conn.close()
    return render_template("products_show.html", product=product)

@app.route("/razotajs/<int:taisitajs_id>")
def razotajs_show(taisitajs_id):
    conn = get_db_connection()
    razotajs = conn.execute("SELECT * FROM taisitajs WHERE id = ?", (taisitajs_id,)).fetchone()
    conn.close()
    return render_template("taisitajs.html", razotajs=razotajs)

@app.route("/krasa/<int:krasa_id>")
def krasa_show(krasa_id):
    conn = get_db_connection()
    krasa = conn.execute("SELECT * FROM krasa WHERE id = ?", (krasa_id,)).fetchone()
    conn.close()
    return render_template("krasa.html", krasa=krasa)

@app.route("/materiali/<int:materiali_id>")
def materiali_show(materiali_id):
    conn = get_db_connection()
    materiali = conn.execute("SELECT * FROM materiali WHERE id = ?", (materiali_id,)).fetchone()
    conn.close()
    return render_template("material.html", materiali=materiali)
@app.route("/produkti")
def products():
    conn = get_db_connection() # Pieslēdzas datubāzei
    # Izpilda SQL vaicājumu, kas atlasa visus produktus
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close() # Aizver savienojumu ar datubāzi

    # conn = sqlite3.connect("miniVeikals.db")      # Izveido savienojumu ar datubāzi miniVeikals.db
    # conn.row_factory = sqlite3.Row   # Uzstāda, lai rindas tiktu atgrieztas kā vārdnīcas
    # cur = conn.cursor()      # Izveido SQL kursoru, ar kuru var izpildīt vaicājumus

    # # Izpilda SQL vaicājumu, kas atlasa visus produktus no tabulas
    # cur.execute(
    #     """
    #     SELECT * FROM products
    #     """
    # )
    # products = cur.fetchall()              # Nolasām visus rezultātus (produktu sarakstu)
    # conn.close()                      # Aizveram savienojumu ar datubāzi
    return render_template("products.html", products=products)     # Atgriežam HTML veidni "products.html", padodot produktus veidnei

@app.route("/par-mums")

def about():
    return render_template("about.html")


from flask import request, redirect, url_for
@app.route("/produkti/new", methods=["GET", "POST"])
def product_create():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        conn = get_db_connection()
        conn.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()
        return redirect(url_for("products"))
    return render_template("product_form.html")


@app.route("/produkti/<int:product_id>/edit", methods=["GET", "POST"])
def edit_product(product_id):
    conn = get_db_connection()
    product = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        conn.execute("UPDATE products SET name = ?, price = ? WHERE id = ?", (name, price, product_id))
        conn.commit()
        conn.close()
        return redirect(url_for("products_show", product_id=product_id))
    conn.close()
    return render_template("product_form.html", product=product)


@app.route("/produkti/<int:product_id>/delete", methods=["POST"])
def delete_product(product_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("products"))




if __name__ == "__main__":
    app.run(debug=True)