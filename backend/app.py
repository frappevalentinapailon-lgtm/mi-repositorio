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
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; box-sizing: border-box; }
                    .success-card { background: white; padding: 40px 30px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; max-width: 400px; width: 100%; }
                    h1 { color: #28a745; margin-bottom: 10px; font-size: 28px; }
                    p { color: #555; margin-bottom: 30px; line-height: 1.5; font-size: 16px; }
                    .btn-volver { background-color: #0056b3; color: white; padding: 14px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px; transition: background 0.3s; display: inline-block; width: 100%; box-sizing: border-box; }
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
    """Pantalla de acceso protegida y responsiva para móviles y PC."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == ADMIN_USER and password == ADMIN_PASS:
            session['admin_logged_in'] = True
            return redirect(url_for('ver_inscritos'))
        else:
            return "<div style='text-align:center; margin-top:50px; font-family:Arial; color:red;'><h3>Credenciales incorrectas.</h3><a href='/login'>Intentar de nuevo</a></div>"
    
    return '''
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Admin LSB - Acceso</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background-color: #f0f2f5;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }
                .login-card {
                    background: white;
                    padding: 40px;
                    border-radius: 12px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                    width: 100%;
                    max-width: 450px; /* Tamaño ideal para PC */
                    box-sizing: border-box;
                    text-align: center;
                }
                h2 { color: #0056b3; margin-bottom: 30px; font-size: 28px; }
                input {
                    width: 100%;
                    padding: 15px; /* Campos amplios para dedos en celular */
                    margin-bottom: 20px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    font-size: 18px; /* Letra legible sin zoom */
                    box-sizing: border-box;
                    outline: none;
                    transition: border-color 0.3s;
                }
                input:focus { border-color: #0056b3; border-width: 2px; }
                button {
                    width: 100%;
                    padding: 16px;
                    background-color: #0056b3;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;
                    transition: background 0.3s, transform 0.2s;
                }
                button:hover { background-color: #004494; transform: translateY(-1px); }
                button:active { transform: translateY(0); }
                .back-link {
                    display: block;
                    margin-top: 25px;
                    color: #666;
                    text-decoration: none;
                    font-size: 16px;
                }
                .back-link:hover { color: #333; text-decoration: underline; }

                /* Ajustes para que en celular se vea a pantalla completa y cómodo */
                @media (max-width: 480px) {
                    .login-card {
                        padding: 30px 20px;
                        border-radius: 0;
                        box-shadow: none;
                        background: transparent;
                    }
                    body { background: white; }
                    h2 { font-size: 24px; }
                }
            </style>
        </head>
        <body>
            <div class="login-card">
                <h2>Admin LSB</h2>
                <form method="post">
                    <input type="email" name="email" placeholder="Correo Electrónico" required>
                    <input type="password" name="password" placeholder="Contraseña" required>
                    <button type="submit">INGRESAR AL PANEL</button>
                </form>
                <a href="/" class="back-link">← Volver al sitio público</a>
            </div>
        </body>
        </html>
    '''

@app.route('/ver-lista-pailon-2026')
def ver_inscritos():
    """Panel de control para ver la lista de inscritos, adaptado a móviles."""
    if not session.get('admin_logged_in'):
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('taller.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inscritos')
    datos = cursor.fetchall()
    conn.close()
    
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <title>Panel Admin - LSB</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f2f5; padding: 20px; margin: 0; }
            .header-admin { display: flex; justify-content: space-between; align-items: center; background: white; padding: 15px 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; flex-wrap: wrap; gap: 10px; }
            h1 { color: #333; margin: 0; font-size: 22px; display: flex; align-items: center; flex-wrap: wrap; gap: 10px; }
            .btn-cerrar { color: #dc3545; text-decoration: none; font-weight: bold; padding: 8px 15px; border: 1px solid #dc3545; border-radius: 5px; transition: 0.3s; }
            .btn-cerrar:hover { background: #dc3545; color: white; }
            
            /* Contenedor para que la tabla se deslice en móviles si es muy ancha */
            .table-responsive { overflow-x: auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
            table { width: 100%; border-collapse: collapse; min-width: 500px; }
            th, td { padding: 15px; text-align: left; border-bottom: 1px solid #ddd; font-size: 15px; }
            th { background-color: #0056b3; color: white; font-weight: 600; }
            tr:hover { background-color: #f9f9f9; }
            
            .contador { background: #ffc107; color: #333; padding: 4px 10px; border-radius: 20px; font-size: 14px; font-weight: bold; white-space: nowrap; }
            
            @media (max-width: 480px) {
                body { padding: 10px; }
                .header-admin { flex-direction: column; align-items: flex-start; }
                .btn-cerrar { width: 100%; text-align: center; box-sizing: border-box; margin-top: 10px; }
            }
        </style>
    </head>
    <body>
        <div class="header-admin">
            <h1>Inscritos Pailón <span class="contador">Total: """ + str(len(datos)) + """</span></h1>
            <a href="/logout" class="btn-cerrar">Cerrar Sesión</a>
        </div>
        
        <div class="table-responsive">
            <table>
                <tr>
                    <th>Nº</th>
                    <th>Nombre Completo</th>
                    <th>Celular / WhatsApp</th>
                    <th>Categoría</th>
                </tr>
    """
    for index, fila in enumerate(datos):
        html += f"<tr><td>{index + 1}</td><td>{fila[1]}</td><td>{fila[2]}</td><td><span style='background:#e9ecef; padding:4px 8px; border-radius:4px; font-size:13px; font-weight:bold;'>{fila[3]}</span></td></tr>"
    
    html += """
            </table>
        </div>
        <p style='color:#666; font-size:14px; text-align:center; margin-top:20px; line-height: 1.5;'>Recuerda copiar o capturar esta lista frecuentemente.</p>
    </body>
    </html>
    """
    return html

@app.route('/logout')
def logout():
    """Cierra la sesión de seguridad."""
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)