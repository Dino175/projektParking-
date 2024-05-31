from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    vozila = conn.execute('SELECT * FROM Vozilo').fetchall()
    parkirna_mjesta = conn.execute('SELECT * FROM ParkirnoMjesto').fetchall()
    conn.close()
    return render_template('index.html', vozila=vozila, parkirna_mjesta=parkirna_mjesta)

@app.route('/vozila', methods=('GET', 'POST'))
def vozila():
    if request.method == 'POST':
        registarska_oznaka = request.form['RegistarskaOznaka']
        marka = request.form['Marka']
        model = request.form['Model']
        boja = request.form['Boja']
        godina_proizvodnje = request.form['GodinaProizvodnje']

        conn = get_db_connection()
        conn.execute('INSERT INTO Vozilo (RegistarskaOznaka, Marka, Model, Boja, GodinaProizvodnje) VALUES (?, ?, ?, ?, ?)',
                     (registarska_oznaka, marka, model, boja, godina_proizvodnje))
        conn.commit()
        conn.close()
        return redirect(url_for('vozila'))

    conn = get_db_connection()
    vozila = conn.execute('SELECT * FROM Vozilo').fetchall()
    conn.close()
    return render_template('vozila.html', vozila=vozila)

@app.route('/parkirna_mjesta', methods=('GET', 'POST'))
def parkirna_mjesta():
    if request.method == 'POST':
        identifikator_mjesta = request.form['IdentifikatorMjesta']
        status = request.form['Status']
        vrijeme_parkiranja = request.form['VrijemeParkiranja']

        conn = get_db_connection()
        conn.execute('INSERT INTO ParkirnoMjesto (IdentifikatorMjesta, Status, VrijemeParkiranja) VALUES (?, ?, ?)',
                     (identifikator_mjesta, status, vrijeme_parkiranja))
        conn.commit()
        conn.close()
        return redirect(url_for('parkirna_mjesta'))

    conn = get_db_connection()
    parkirna_mjesta = conn.execute('SELECT * FROM ParkirnoMjesto').fetchall()
    conn.close()
    return render_template('parkirna_mjesta.html', parkirna_mjesta=parkirna_mjesta)

if __name__ == "__main__":
    app.run(debug=True)
