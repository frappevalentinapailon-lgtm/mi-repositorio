from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

app = Flask(__name__, 
            template_folder='../frontend', 
            static_folder='../frontend',
            static_url_path='')

app.secret_key = 'lsb_pailon_2026_secret_key'

ADMIN_USER = "admin@lsb.com"
ADMIN_PASS = "12345"

def init_db():
    """Crea la tabla de inscritos si no existe."""
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

# SOLUCIÓN AL ERROR 500: Ejecutamos la función aquí mismo para que Render la lea sí o sí.
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    nombre = request.form.get('nombre')
    whatsapp = request.form.get('whatsapp')
    categoria = request.form.get('categoria')

    if nombre and whatsapp:
        try:
            conn = sqlite3.connect('taller.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO inscritos (nombre, whatsapp, categoria) VALUES (?, ?, ?)', 
                           (nombre, whatsapp, categoria))
            conn.commit()
            conn.close()
            return "¡Inscripción exitosa! Nos pondremos en contacto contigo pronto. <br><a href='/'>Volver al inicio</a>"
        except Exception as e:
            # Si hay otro error interno, ahora te mostrará qué es exactamente
            return f"Ocurrió un error al guardar: {e}", 500
            
    return "Error: Faltan datos importantes.", 400

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for('ver_inscritos'))
        else:
            return "Credenciales incorrectas. Intenta de nuevo."
    
    return '''
        <div style="max-width:300px; margin:100px auto; text-align:center; font-family:Arial; padding:20px; border:1px solid #ddd; border-radius:10px;">
            <h2>Admin LSB</h2>
            <form method="post">
                <input type="email" name="email" placeholder="Correo" style="width:100%; padding:10px; margin-bottom:10px;" required><br>
                <input type="password" name="password" placeholder="Contraseña" style="width:100%; padding:10px; margin-bottom:10px;" required><br>
                <button type="submit" style="width:100%; padding:10px; background:#0056b3; color:white; border:none; cursor:pointer;">Entrar</button>
            </form>
        </div>
    '''

@app.route('/ver-lista-pailon-2026')
def ver_inscritos():
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('taller.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inscritos')
    datos = cursor.fetchall()
    conn.close()
    
    html = """
    <html>
    <head><title>Panel Admin - LSB</title></head>
    <body style="font-family: Arial; padding: 20px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h1>Lista de Inscritos - Pailón 2026</h1>
            <a href="/logout" style="color:red; text-decoration:none; font-weight:bold;">Cerrar Sesión</a>
        </div>
        <table border="1" style="width:100%; border-collapse: collapse; margin-top:20px;">
            <tr style="background: #f0f2f5; text-align:left;">
                <th style="padding:10px;">ID</th>
                <th style="padding:10px;">Nombre Completo</th>
                <th style="padding:10px;">WhatsApp</th>
                <th style="padding:10px;">Categoría</th>
            </tr>
    """
    for fila in datos:
        html += f"<tr><td style='padding:10px;'>{fila[0]}</td><td style='padding:10px;'>{fila[1]}</td><td style='padding:10px;'>{fila[2]}</td><td style='padding:10px;'>{fila[3]}</td></tr>"
    
    html += "</table><p>Recuerda copiar estos datos a Excel frecuentemente.</p></body></html>"
    return html

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)