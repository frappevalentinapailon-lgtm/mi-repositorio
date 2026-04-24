from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
import os

# Configuración de Flask para reconocer la carpeta frontend
app = Flask(__name__, 
            template_folder='../frontend', 
            static_folder='../frontend',
            static_url_path='')

# Clave de seguridad para proteger el acceso al panel de administrador
app.secret_key = 'lsb_pailon_2026_secret_key'

# Credenciales de Administrador exclusivas
ADMIN_USER = "admin@lsb.com"
ADMIN_PASS = "12345"

def init_db():
    """Crea la base de datos y la tabla si no existen."""
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

# ¡IMPORTANTE! Ejecutamos la función aquí para evitar el Error 500 en Render
init_db()

@app.route('/')
def index():
    """Muestra la página de inicio con el formulario."""
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar():
    """Recibe los datos, los guarda y muestra el mensaje de éxito."""
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
            
            # Pantalla de Éxito Centrada y Profesional
            return """
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>¡Inscripción Exitosa!</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; }
                    .success-card { background: white; padding: 40px 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; max-width: 400px; width: 90%; }
                    h1 { color: #28a745; margin-bottom: 10px; font-size: 28px; }
                    p { color: #555; margin-bottom: 30px; line-height: 1.5; font-size: 16px; }
                    .btn-volver { background-color: #0056b3; color: white; padding: 12px 25px; text-decoration: none; border-radius: 6px; font-weight: bold; transition: background 0.3s; display: inline-block; width: 100%; box-sizing: border-box; }
                    .btn-volver:hover { background-color: #004494; }
                </style>
            </head>
            <body>
                <div class="success-card">
                    <h1>¡Registro Exitoso! 🎉</h1>
                    <p>Tus datos han sido guardados correctamente para el Taller de LSB en Pailón. Nos pondremos en contacto contigo pronto.</p>
                    <a href="/" class="btn-volver">Volver al formulario</a>
                </div>
            </body>
            </html>
            """
        except Exception as e:
            return f"<div style='text-align:center; margin-top:50px; font-family:Arial;'><h3>Ocurrió un error al guardar:</h3><p>{e}</p><a href='/'>Volver</a></div>", 500
            
    return "<div style='text-align:center; margin-top:50px; font-family:Arial;'><h3>Error: Faltan datos importantes.</h3><a href='/'>Volver</a></div>", 400

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Pantalla de acceso protegida."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for('ver_inscritos'))
        else:
            return "<div style='text-align:center; margin-top:50px; font-family:Arial; color:red;'><h3>Credenciales incorrectas.</h3><a href='/login'>Intentar de nuevo</a></div>"
    
    return '''
        <div style="max-width:320px; margin:10vh auto; text-align:center; font-family:Arial; padding:30px; background:white; border-radius:10px; box-shadow:0 4px 15px rgba(0,0,0,0.1);">
            <h2 style="color:#0056b3; margin-bottom:20px;">Admin LSB</h2>
            <form method="post">
                <input type="email" name="email" placeholder="Correo Electrónico" style="width:100%; padding:12px; margin-bottom:15px; border:1px solid #ddd; border-radius:6px; box-sizing:border-box;" required>
                <input type="password" name="password" placeholder="Contraseña" style="width:100%; padding:12px; margin-bottom:20px; border:1px solid #ddd; border-radius:6px; box-sizing:border-box;" required>
                <button type="submit" style="width:100%; padding:12px; background:#0056b3; color:white; border:none; border-radius:6px; font-size:16px; cursor:pointer; font-weight:bold;">Ingresar</button>
            </form>
            <a href="/" style="display:block; margin-top:15px; color:#777; text-decoration:none; font-size:14px;">← Volver al sitio público</a>
        </div>
    '''

@app.route('/ver-lista-pailon-2026')
def ver_inscritos():
    """Panel de control para ver la lista de inscritos."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('taller.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inscritos')
    datos = cursor.fetchall()
    conn.close()
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Panel Admin - LSB</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 20px; margin: 0; }
            .header-admin { display: flex; justify-content: space-between; align-items: center; background: white; padding: 15px 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; }
            h1 { color: #333; margin: 0; font-size: 24px; }
            .btn-cerrar { color: #dc3545; text-decoration: none; font-weight: bold; padding: 8px 15px; border: 1px solid #dc3545; border-radius: 5px; transition: 0.3s; }
            .btn-cerrar:hover { background: #dc3545; color: white; }
            table { width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-radius: 8px; overflow: hidden; }
            th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #0056b3; color: white; font-weight: 600; }
            tr:hover { background-color: #f9f9f9; }
            .contador { background: #ffc107; color: #333; padding: 5px 10px; border-radius: 20px; font-size: 14px; font-weight: bold; margin-left: 10px; }
        </style>
    </head>
    <body>
        <div class="header-admin">
            <h1>Inscritos LSB Pailón <span class="contador">Total: """ + str(len(datos)) + """</span></h1>
            <a href="/logout" class="btn-cerrar">Cerrar Sesión</a>
        </div>
        <table>
            <tr>
                <th>Nº</th>
                <th>Nombre Completo</th>
                <th>Celular / WhatsApp</th>
                <th>Categoría</th>
            </tr>
    """
    for index, fila in enumerate(datos):
        html += f"<tr><td>{index + 1}</td><td>{fila[1]}</td><td>{fila[2]}</td><td><span style='background:#e9ecef; padding:4px 8px; border-radius:4px; font-size:13px;'>{fila[3]}</span></td></tr>"
    
    html += "</table><p style='color:#666; font-size:14px; text-align:center; margin-top:20px;'>Recuerda copiar o capturar esta lista frecuentemente.</p></body></html>"
    return html

@app.route('/logout')
def logout():
    """Cierra la sesión de seguridad."""
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)