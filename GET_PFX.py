from cryptography.hazmat.primitives import serialization
import cryptography.x509   # just to get random serial number
import PySimpleGUI as sg
import secrets
import CAsigningcert
import Credentials as secu
import send_mail
from OpenSSL import crypto

CA_crt = crypto.x509.load_pem_x509_certificate(bytes.fromhex(secu.main_cert).decode().encode())
CA_Private = serialization.load_pem_private_key(bytes.fromhex(secu.main_priv).decode().encode(),password=None)
private_key = crypto.PKey().from_cryptography_key(CA_Private)


def req_pfx_from_ca(algo:str,sub_name:str,sub_alt_name:str,validity_in_months:int,path_to_store:str,protect:bool):

    phi = secrets.token_urlsafe(8)

    def sub_alt_sep(sample: str):
        if sample == "": return None
        if sample is None: return None
        res = "";sam_lis = sample.split(";");num = len(sam_lis)
        for i in range(num):
            if i < num - 1:
                res += "DNS:" + sam_lis[i] + ","
            else:
                res += "DNS:" + sam_lis[i]
        return res

    key = crypto.PKey(); vali = 1
    if algo == "RSA" : key.generate_key(crypto.TYPE_RSA, 2048)
    if algo == "DSA" : key.generate_key(crypto.TYPE_DSA, 2048)
    cert = crypto.X509()
    cert.get_subject().CN = sub_name
    cert.add_extensions([crypto.X509Extension(b'extendedKeyUsage', True, b'serverAuth,clientAuth')])
    if sub_alt_sep(sub_alt_name) is not None:
        cert.add_extensions([crypto.X509Extension(b'subjectAltName', False, sub_alt_sep(sub_alt_name).encode())])
    cert.set_issuer(crypto.X509.from_cryptography(CA_crt).get_issuer())
    cert.set_serial_number(cryptography.x509.random_serial_number())
    if validity_in_months == 3: vali = 4
    if validity_in_months == 6: vali = 2
    if validity_in_months == 12: vali = 1
    cert.gmtime_adj_notBefore(0); cert.gmtime_adj_notAfter(int((365*24*60*60)/vali))
    cert.set_pubkey(key)
    cert.sign(private_key,'sha256')
    #open(path_to_store+"\certificate.cer", 'w').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())
    #open(path_to_store+"\private_key.pem", 'w').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode())
    p12 = crypto.PKCS12()
    p12.set_privatekey(key)
    p12.set_certificate(cert)
    p12.set_ca_certificates([crypto.X509.from_cryptography(CA_crt)])
    if protect:
        open(path_to_store+"\PKCS12_format.pfx", 'wb').write(p12.export(passphrase=phi))
    else:
        open(path_to_store + "\PKCS12_format.pfx", 'wb').write(p12.export(passphrase=None))


def reqPFX_gui():
    mail_layou1 = [[sg.Text(text="Enter recipient mail ids here:")],
                   [sg.Input(tooltip="for multiple ids separate with comma", key="mails", enable_events=True)],
                   [sg.Text(text="")],
                   [sg.Button(button_text="Share", key="shr", pad=((130, 0), (0, 0)))],
                   ]
    mail_windo = sg.Window(title="Sharing Certificate", layout=mail_layou1,icon=secu.icon_base64)

    layout = [[sg.Text("PKCS#12 from CA",font="Any 14",pad=((80,0),(0,0)))],[sg.Text("")],
              [sg.Text('Fill the details to generate PFX', font='Any 11')],[sg.Text("")],
              [sg.Text("Common Name*: "),sg.Input(key="CN",size=(19,1))],[sg.Text("")],
              [sg.Text("Sub. Alt Names:"),sg.Input(key="alt_names",size=(30,10),tooltip="separate with ; for multiple values")],[sg.Text("")],
              [sg.Text("Key Algorithm: "),sg.Combo(["RSA","DSA"], default_value="RSA", key="algo")],[sg.Text("")],
              [sg.Text("Validity: "), sg.Combo(["3 months","6 months","1 year"], default_value="1 Year", key="valy")],[sg.Text("")],
              [sg.Checkbox("Protect with password",key="pas")],[sg.Text("")],
              [sg.Text("Add Root to Trust-store : ",text_color="orange",font="Any 12"),sg.Button(button_text="Add",auto_size_button=True,button_color="grey",enable_events=True,key="adtrust")],
              [sg.Text("")],
              [sg.Input(visible=False, key="tr", enable_events=True),
               sg.FolderBrowse(button_text="Download", auto_size_button=True, key="savi",enable_events=True),sg.Text("         "),
               sg.Button(button_text="Share via mail", key="mail"),sg.Text("             "),sg.Exit(key="quit",button_color='red')]
              ]
    window = sg.Window(title="Pfx",layout=layout,icon=secu.icon_base64)
    while True:
        event,value = window.read()
        if event in ("quit",sg.WIN_CLOSED):
            break
        if event == "tr":
            req_pfx_from_ca(algo=value["algo"], sub_name=value["CN"], sub_alt_name=value["alt_names"],
                            validity_in_months=value["valy"],path_to_store=value["savi"],protect=value["pas"])
        if event == "mail":
            req_pfx_from_ca(algo=value["algo"], sub_name=value["CN"], sub_alt_name=value["alt_names"],
                            validity_in_months=value["valy"], path_to_store=value["savi"], protect=value["pas"])
            while True:
                events,values = mail_windo.read()
                if events == sg.WIN_CLOSED:
                    break
                if events == "adtrust":
                    try:
                        CAsigningcert.CAsigning.addtotrust()
                    except:
                        pass
                if events == "shr":
                    try:
                        send_mail.send_mail_pfx(value["savi"]+"\\PKCS12_format",receiver_mail=values["mails"])
                        sg.popup_no_buttons("shared successfully", auto_close=True, no_titlebar=True,
                                                        background_color="green", relative_location=(70, 70))
                        break
                    except:
                        sg.popup_no_buttons("Give proper mail ids", auto_close=True, no_titlebar=True,
                                                        background_color="red",relative_location=(70, 70))
                        break


#req_pfx_from_ca(algo="RSA",sub_name="teja.happy.net",sub_alt_name="teja.net;nike.net",validity_in_months=6,path_to_store="D:\Lasya files\pfx_testing\signed_CA",protect=False)

