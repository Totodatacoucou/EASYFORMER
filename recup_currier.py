import imaplib
import email
import os

# Informations de connexion à la boîte e-mail Gmail
EMAIL = 'easy.test.code@gmail.com'
PASSWORD = 'Rexona76'
SERVER = 'imap.gmail.com'

# Se connecter au serveur IMAP de Gmail
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

# Chemin vers le dossier de destination sur Jenkins
dossier_destination = "http://localhost:8080/job/RECUP_COURRIER/"

# Rechercher les e-mails avec l'objet "rédacteur"
status, messages = mail.search(None, '(SUBJECT "rédacteur")')

for num in messages[0].split():
    status, data = mail.fetch(num, '(RFC822)')
    msg = email.message_from_bytes(data[0][1])
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()
        if filename:
            # Construire le chemin local basé sur l'URL de Jenkins
            chemin_fichier = os.path.join(dossier_destination, filename)
            with open(chemin_fichier, 'wb') as f:
                f.write(part.get_payload(decode=True))

# Se déconnecter du serveur IMAP de Gmail
mail.close()
mail.logout()
