import smtplib
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIGURAÇÃO (Preencha aqui ou via variáveis de ambiente) ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "seu-email@gmail.com")
SENDER_PASSWORD = os.environ.get("SENDER_PASSWORD", "sua-senha-de-app")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "seu-email@gmail.com")

def get_urls():
    links = {"dash": "", "vnc": ""}
    try:
        with open("/home/opc/litemode/tunnel.log", "r") as f:
            match = re.search(r"https://[a-zA-Z0-9.-]+\.trycloudflare\.com", f.read())
            if match: links["dash"] = match.group(0)
            
        with open("/home/opc/litemode/tunnel-vnc.log", "r") as f:
            match = re.search(r"https://[a-zA-Z0-9.-]+\.trycloudflare\.com", f.read())
            if match: links["vnc"] = match.group(0)
    except Exception as e:
        print(f"Erro ao ler logs: {e}")
    return links

def send_email():
    urls = get_urls()
    if not urls["dash"] or not urls["vnc"]:
        print("Links ainda não gerados. Abortando envio de e-mail.")
        return

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = "🚀 LiteMode: Seus links de acesso remoto"

    body = f"""
    Olá! Seus serviços LiteMode foram iniciados com sucesso.

    📊 Dashboard de Gerenciamento: {urls['dash']}
    🖥️ Desktop Remoto (noVNC): {urls['vnc']}/vnc.html

    ---
    Gerado automaticamente pela instância Oracle Cloud.
    """
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Falha ao enviar e-mail: {e}")

if __name__ == "__main__":
    send_email()
