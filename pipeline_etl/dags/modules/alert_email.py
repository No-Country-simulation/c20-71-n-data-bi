import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
from parameters import SENDER_EMAIL, RECEIVER_EMAIL, PASSWORD_EMAIL

# from dotenv import load_dotenv
# import os

# dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
# load_dotenv(dotenv_path)

def send_email(subject, body):
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('PASSWORD_EMAIL')
    
    # Crear el objeto del mensaje
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Agregar el cuerpo del mensaje al email
    msg.attach(MIMEText(body, 'plain'))

    # Crear la conexión segura con el servidor y enviar el email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Correo enviado exitosamente!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def check_for_significant_variation(data, previous_data, threshold=0.20):
    """
    Comprueba si hay una variación significativa en los datos en comparación con los datos anteriores.
    Envía alertas si la variación es superior al umbral especificado.
    
    :param data: DataFrame con los datos actuales.
    :param previous_data: DataFrame con los datos anteriores.
    :param threshold: Umbral de variación (por defecto es 20%).
    """
    data = data.set_index('Date')  # Ajusta la columna de fecha según sea necesario
    previous_data = previous_data.set_index('Date')

    for column in data.columns:
        if column != 'Date':  # Excluye la columna de fecha
            current_values = data[column]
            previous_values = previous_data[column]
            
            # Verifica si las columnas están alineadas
            if not current_values.index.equals(previous_values.index):
                raise ValueError("Las fechas en los datos actuales y anteriores no coinciden.")
            
            # Calcula la variación porcentual
            variation = (current_values - previous_values) / previous_values
            
            # Filtra las variaciones significativas
            significant_changes = variation[abs(variation) > threshold]
            
            if not significant_changes.empty:
                subject = f"Alerta de Variación Significativa para {column}"
                body = f"Se han detectado variaciones significativas en los valores de {column}:\n\n{significant_changes}"
                send_email(subject, body)
                print(f"Alerta enviada debido a variaciones significativas en {column}.")

# Ejemplo de uso
# current_data = pd.read_csv('datasets/current_data.csv')
# previous_data = pd.read_csv('datasets/previous_data.csv')
# check_for_significant_variation(current_data, previous_data)
