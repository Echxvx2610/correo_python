from flask import Flask, request, jsonify
from flask_cors import CORS  # Importamos CORS
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import os  # Importamos os para acceder a las variables de entorno
from dotenv import load_dotenv  # Importamos load_dotenv para cargar las variables del archivo .env


app = Flask(__name__)

# Habilitar CORS para todas las rutas
CORS(app)



# Cargar las variables de entorno del archivo .env
load_dotenv()

# Ahora puedes acceder a las variables de entorno con os.getenv()
gmail_user = os.getenv('GMAIL_USER')
gmail_password = os.getenv('GMAIL_PASSWORD')

@app.route('/send_order', methods=['POST'])
def send_order():
    data = request.get_json()
    if not data:
        return {'error': 'No se recibieron datos'}, 400
    
    item = data.get('item', '')
    quantity = data.get('quantity', '')
    customer_name = data.get('customer_name', '')

    if not item or not quantity or not customer_name:
        return {'error': 'Faltan datos del pedido'}, 400

    # Crear el cuerpo del mensaje en HTML
    subject = 'Nuevo Pedido'
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #2d87f0;">Nuevo Pedido</h2>
        <p><strong>Cliente:</strong> {customer_name}</p>
        <p><strong>Producto:</strong> {item}</p>
        <p><strong>Cantidad:</strong> {quantity}</p>
    </body>
    </html>
    """
    
    # Crear el mensaje MIME
    message = MIMEMultipart()
    message['From'] = gmail_user
    message['To'] = gmail_user
    message['Subject'] = Header(subject, 'utf-8')  # Codificamos el encabezado del asunto

    # Adjuntar el cuerpo del mensaje con la codificación UTF-8
    message.attach(MIMEText(body, 'html', 'utf-8'))

    try:
        # Enviar el correo electrónico
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_password)
            server.sendmail(gmail_user, gmail_user, message.as_string())
            return {'message': 'Pedido enviado por correo electrónico'}, 200
    except Exception as e:
        print(f"Error al enviar el correo: {str(e)}")
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
