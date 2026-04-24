from flask import Flask, render_template, request
import sqlite3
import os

# Configuramos Flask para que mire hacia la carpeta 'frontend'
app = Flask(__name__, 
            template_folder='../frontend', 
            static_folder='../frontend',
            static_url_path='')

def init_db():
    conn = sqlite3.connect('taller.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscritos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            whatsapp TEXT NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre')
    whatsapp = request.form.get('whatsapp')
    categoria = request.form.get('categoria')

    conn = sqlite3.connect('taller.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO inscritos (nombre, whatsapp, categoria) VALUES (?, ?, ?)', 
                   (nombre, whatsapp, categoria))
    conn.commit()
    conn.close()
    
    return "¡Registro recibido exitosamente! Nos contactaremos contigo pronto."

if __name__ == '__main__':
    init_db()
    app.run(debug=True)