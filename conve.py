from cryptography.hazmat.primitives import serialization
import cryptography
import Credentials as secu
from OpenSSL import crypto
import secrets, PySimpleGUI as sg

def crt_to_pfx(certificate:str,private_key:str,ca_chain:str,path_down:str,prot:bool):

    p12 = crypto.PKCS12()
    pr = cryptography.hazmat.primitives.serialization.load_pem_private_key(private_key.encode(), password=None)
    p12.set_privatekey(crypto.PKey().from_cryptography_key(pr))
    p12.set_certificate(crypto.X509.from_cryptography(crypto.x509.load_pem_x509_certificate(certificate.encode())))
    if ca_chain != "":
        p12.set_ca_certificates(
            [crypto.X509.from_cryptography(crypto.x509.load_pem_x509_certificate(ca_chain.encode()))])
    if prot:
        open(path_down+"\PFX_Format.pfx","wb").write(p12.export(passphrase=secrets.token_urlsafe(8).encode()))
    else:
        open(path_down+"\PFX_Format.pfx", "wb").write(p12.export(passphrase=None))

def conve_ui_pfx():

    layou = [[sg.Text("Certificate to PFX",font="Any 12",pad=((200,0),(0,0)))],
             [sg.Text()],
             [sg.Text("Upload Certificate (in pem or txt):  "),sg.InputText(key="-pat-",enable_events=True),
              sg.FileBrowse(file_types=(("Text Files", "*.txt"),("Crt Files", "*.crt"),("Cer Files", "*.cer"),("PEM files",".pem"),))],
             [sg.Text("Upload private_Key (in pem or txt):"), sg.InputText(key="-pat-priv",enable_events=True),
              sg.FileBrowse(file_types=(("Text Files", "*.txt"),("Key Files", "*.key"),("PEM files", ".pem"),))],
             [sg.Text("Upload Chain File (optional) :        "), sg.InputText(key="-pat-chi",default_text="",enable_events=True),
              sg.FileBrowse(file_types=(("Text Files", "*.txt"), ("PEM files", ".pem"),))],
             [sg.Text()],
             [sg.Checkbox(text="Password protected",key="chl")],[sg.Text()],
             [sg.Input(visible=False, key="tr", enable_events=True),
              sg.FolderBrowse(button_text="Download PFX",key="down_pfx",enable_events=True),sg.Exit(button_color="red",pad=((480,0),(0,0)))]
            ]

    windi = sg.Window(title="Download PFX",layout=layou,icon=secu.icon_base64)

    while True:
        events,values = windi.read()
        if events in ("Exit",sg.WIN_CLOSED):
            windi.close();break
        if events == "tr":
             try:
                cert_sr = open(values["-pat-"], "r").read()
                priv_sr = open(values["-pat-priv"],"r").read()
                if values["-pat-chi"] == "":
                    crt_to_pfx(cert_sr,priv_sr
                               , ca_chain="", prot=values["chl"], path_down=values["down_pfx"])
                else:
                    chain_sr = open(values["-pat-chi"],"r").read()
                    crt_to_pfx(cert_sr,priv_sr
                               ,ca_chain=chain_sr,prot=values["chl"],path_down=values["down_pfx"])
                sg.popup_no_buttons("Downloaded", auto_close=True, no_titlebar=True,
                                    background_color="green", relative_location=(70, 70))
                windi.close()
             except:
                 sg.popup_no_buttons("provide proper path", auto_close=True, no_titlebar=True,
                                     background_color="red", relative_location=(70, 70))

# hi = crypto.PKCS12()
# pri = cryptography.hazmat.primitives.serialization.load_pem_private_key(open(r"D:\Surya_files\pfx_testing\private_key.pem","r").read().encode(),password=None)
# hi.set_certificate(crypto.X509.from_cryptography(crypto.x509.load_pem_x509_certificate(open(r"D:\Surya_files\pfx_testing\certificate.cer","r").read().encode())))
# hi.set_privatekey(crypto.PKey().from_cryptography_key(pri))
# hi.set_ca_certificates([crypto.X509.from_cryptography(crypto.x509.load_pem_x509_certificate(bytes.fromhex(secu.main_cert).decode().encode()))])
# open(r"D:\Surya_files\pfx_testing\signed_CA\PFX_format.pfx","wb").write(hi.export(passphrase=None))

# crti = open("D:\Surya_files\pfx_testing\certificate.cer","r").read()
# p = open("D:\Surya_files\pfx_testing\private_key.pem","r").read()
#
# crt_to_pfx(crti,p,ca_chain="",path_down="D:\Surya_files\pfx_testing\signed_CA",prot=False)
#

