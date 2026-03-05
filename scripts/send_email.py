import smtplib
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification(dashboard_url, vnc_url):
    sender_email = "jeronimo.moraes.gomes@gmail.com"
    receiver_email = "jeronimo.gomes@marinha.mil.br"
    password = "glzh zuqu ervs yqbs" # App Password

    message = MIMEMultipart("alternative")
    message["Subject"] = "🚀 LiteMode: Serviços Iniciados com Sucesso!"
    message["From"] = f"LiteMode Admin <{sender_email}>"
    message["To"] = receiver_email

    text = f"""
    Olá, os serviços do LiteMode foram iniciados.

    Dashboard: {dashboard_url}
    Desktop (noVNC): {vnc_url}/vnc.html

    Atenciosamente,
    LiteMode System
    """

    html = f"""
    <html>
      <body style="font-family: sans-serif; color: #333;">
        <h2 style="color: #3b82f6;">🚀 LiteMode: Serviços Online</h2>
        <p>Os serviços do sistema foram iniciados e estão prontos para acesso.</p>
        <div style="background: #f1f5f9; padding: 20px; border-radius: 8px;">
          <p><strong>Dashboard de Gerenciamento:</strong><br>
          <a href="{dashboard_url}" style="color: #3b82f6;">{dashboard_url}</a></p>
          <p><strong>Desktop Remoto (noVNC):</strong><br>
          <a href="{vnc_url}/vnc.html" style="color: #3b82f6;">{vnc_url}/vnc.html</a></p>
        </div>
        <p style="font-size: 0.8em; color: #64748b; margin-top: 20px;">
          Oracle Instance Lite Remote Access
        </p>
      </body>
    </html>
    """

    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("E-mail de notificação enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 send_email.py <dashboard_url> <vnc_url>")
        sys.exit(1)
    
    send_notification(sys.argv[1], sys.argv[2])
