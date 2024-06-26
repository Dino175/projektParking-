from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import sqlite3
import string
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
DATABASE = 'database.sqlite'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def generate_parking_spots():
    conn = get_db_connection()
    zauzeta_mjesta = [mjesto['IdentifikatorMjesta'] for mjesto in conn.execute('SELECT IdentifikatorMjesta FROM ParkirnoMjesto WHERE Status = "zauzeto"').fetchall()]
    conn.close()
    
    spots = []
    for letter in string.ascii_lowercase[:6]:
        for number in range(1, 10):
            spot = f"{letter}{number}"
            if spot not in zauzeta_mjesta:
                spots.append(spot)
    return spots

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
        vozilo = conn.execute('SELECT * FROM Vozilo WHERE RegistarskaOznaka = ?', (registarska_oznaka,)).fetchone()
        
        if vozilo is not None:
            conn.close()
            flash('Vozilo s istom registarskom oznakom već postoji!')
            return redirect(url_for('vozila'))

        conn.execute('INSERT INTO Vozilo (RegistarskaOznaka, Marka, Model, Boja, GodinaProizvodnje) VALUES (?, ?, ?, ?, ?)',
                     (registarska_oznaka, marka, model, boja, godina_proizvodnje))
        conn.commit()
        conn.close()
        return redirect(url_for('parkirna_mjesta'))

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
        existing_spot = conn.execute('SELECT * FROM ParkirnoMjesto WHERE IdentifikatorMjesta = ?', (identifikator_mjesta,)).fetchone()
        conn.close()

        if existing_spot:
            flash('This parking spot is already taken.')
            return redirect(url_for('parkirna_mjesta'))

        conn = get_db_connection()
        conn.execute('INSERT INTO ParkirnoMjesto (IdentifikatorMjesta, Status, VrijemeParkiranja) VALUES (?, ?, ?)',
                     (identifikator_mjesta, status, vrijeme_parkiranja))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    spots = generate_parking_spots()
    conn = get_db_connection()
    parkirna_mjesta = conn.execute('SELECT * FROM ParkirnoMjesto').fetchall()
    conn.close()
    return render_template('parkirna_mjesta.html', parkirna_mjesta=parkirna_mjesta, spots=spots)

@app.route('/vozila/edit/<string:RegistarskaOznaka>', methods=['GET', 'POST'])
def edit_vozilo(RegistarskaOznaka):
    conn = get_db_connection()
    vozilo = conn.execute('SELECT * FROM Vozilo WHERE RegistarskaOznaka = ?', (RegistarskaOznaka,)).fetchone()
    conn.close()
    if request.method == 'POST':
        marka = request.form['Marka']
        model = request.form['Model']
        boja = request.form['Boja']
        godina_proizvodnje = request.form['GodinaProizvodnje']

        conn = get_db_connection()
        conn.execute('UPDATE Vozilo SET Marka = ?, Model = ?, Boja = ?, GodinaProizvodnje = ? WHERE RegistarskaOznaka = ?',
                     (marka, model, boja, godina_proizvodnje, RegistarskaOznaka))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('edit_vozilo.html', vozilo=vozilo)

@app.route('/api/parkirna_mjesta')
def get_parking_spots():
    conn = get_db_connection()
    parkirna_mjesta = conn.execute('SELECT * FROM ParkirnoMjesto').fetchall()
    conn.close()
    
    current_time = datetime.now().time()
    updated_spots = []
    for mjesto in parkirna_mjesta:
        vrijeme_parkiranja = datetime.strptime(mjesto['VrijemeParkiranja'], "%H.%M").time()
        if current_time > vrijeme_parkiranja and mjesto['Status'] == 'zauzeto':
            mjesto['Status'] = 'slobodno'
        
        updated_spots.append(dict(mjesto))
    
    return jsonify({'parkirna_mjesta': updated_spots})

@app.route('/api/slobodna_mjesta')
def api_slobodna_mjesta():
    spots = generate_parking_spots()
    return jsonify({'slobodna_mjesta': spots})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
