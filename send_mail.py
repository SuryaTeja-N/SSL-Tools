import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import Credentials as secu
from zipfile import ZipFile

def send_mail(zip_path:str,receiver_mail:str):

    fromaddr = bytes.fromhex(secu.from_send).decode()
    toaddr = receiver_mail

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "signed SSL certificate"

    body = "Please find attached certificate files as per your request 😊 and thanks for testing 🥰"

    msg.attach(MIMEText(body, 'plain'))

    attachment = open(zip_path+".zip", "rb")

    part = MIMEBase('application', "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % ("Certificates"+ '.zip'))

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, bytes.fromhex(secu.send_pass).decode())
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def send_mail_pfx(pfx_path:str, receiver_mail:str):
    fromaddr = bytes.fromhex(secu.from_send).decode()
    toaddr = receiver_mail

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "PFX form CA"

    body = "Please find attached PKCS#12 file as per your request 😊 and thanks for testing 🥰"

    msg.attach(MIMEText(body, 'plain'))

    attachment = open(pfx_path + ".pfx", "rb")

    part = MIMEBase('application', "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % ("PKCS12_certificate" + '.pfx'))

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, bytes.fromhex(secu.send_pass).decode())
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

def send_code_files(files_string:str,requester_mail:str):

    files_lit = files_string.split(";")

    with ZipFile(r'D:\CodeSign_files_upload.zip', 'w') as myzip:
        for i in files_lit:
            myzip.write(i)

    fromaddr = bytes.fromhex(secu.from_send).decode(); toaddr = bytes.fromhex(secu.receiver_pass).decode()
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Code_Sign request"

    body = "Requester mail id is : " + requester_mail

    msg.attach(MIMEText(body, 'plain'))
    attachment = open(r'D:\CodeSign_files_upload.zip', "rb")

    part = MIMEBase('application', "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % ("CodeSign_request" + '.zip'))

    msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, bytes.fromhex(secu.send_pass).decode())
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

