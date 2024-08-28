import hashlib
import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
URL = "http://votre-site.com/index.html"  # Remplacez par l'URL de votre page index.html
CHECK_INTERVAL = 600  # 10 minutes en secondes
REFERENCE_HASH_FILE = "reference_hash.txt"

# Configuration email
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "votre-email@gmail.com"
SENDER_PASSWORD = "votre-mot-de-passe"
RECEIVER_EMAIL = "destinataire@example.com"

def get_page_content(url):
    response = requests.get(url)
    return response.text

def calculate_hash(content):
    return hashlib.sha256(content.encode()).hexdigest()

def send_email_alert(new_hash):
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = "Alerte : Modification détectée sur index.html"
    
    body = f"Une modification a été détectée sur la page index.html.\nNouveau hash : {new_hash}"
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(message)

def main():
    try:
        with open(REFERENCE_HASH_FILE, "r") as f:
            reference_hash = f.read().strip()
    except FileNotFoundError:
        content = get_page_content(URL)
        reference_hash = calculate_hash(content)
        with open(REFERENCE_HASH_FILE, "w") as f:
            f.write(reference_hash)

    while True:
        content = get_page_content(URL)
        current_hash = calculate_hash(content)

        if current_hash != reference_hash:
            print("Modification détectée ! Envoi d'une alerte par email.")
            send_email_alert(current_hash)
            reference_hash = current_hash
            with open(REFERENCE_HASH_FILE, "w") as f:
                f.write(reference_hash)
        else:
            print("Aucune modification détectée.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
