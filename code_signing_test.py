from cryptography.hazmat.primitives import serialization

import CAsigningcert
import Credentials as secu
import PySimpleGUI as sg
from OpenSSL import crypto
import cryptography.x509
import send_mail,os

CA_crt = crypto.x509.load_pem_x509_certificate(bytes.fromhex(secu.main_cert).decode().encode())
CA_Private = serialization.load_pem_private_key(bytes.fromhex(secu.main_priv).decode().encode(),password=None)
private_key = crypto.PKey().from_cryptography_key(CA_Private)

def gen_codesigncert(cn_name:str,path_to_store:str):
    code_cert = crypto.X509()
    code_cert.get_subject().CN = cn_name

    code_cert.add_extensions([crypto.X509Extension(b'extendedKeyUsage', True, b'codeSigning')])
    code_cert.set_issuer(crypto.X509.from_cryptography(CA_crt).get_issuer())
    code_cert.set_serial_number(cryptography.x509.random_serial_number())
    code_cert.set_issuer(crypto.X509.from_cryptography(CA_crt).get_issuer())
    code_cert.gmtime_adj_notBefore(0); code_cert.gmtime_adj_notAfter(int(365*24*60*60))
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_DSA,2048)
    code_cert.set_pubkey(key)
    code_cert.sign(private_key,'sha256')
    #open("D:\Lasya files\pfx_testing\signed_CA\sign_codecert.crt","w").write(crypto.dump_certificate(crypto.FILETYPE_PEM,code_cert).decode())
    codesign_pfx = crypto.PKCS12()
    codesign_pfx.set_certificate(code_cert);codesign_pfx.set_privatekey(key)
    open(path_to_store+"\\CodeSign_cert.pfx","wb").write(crypto.PKCS12.export(codesign_pfx,passphrase=None))

def Getyour_code_sign():
    pass

def codesign_gui():

    def mail_gui():
        mail_layout = [[sg.Text("Upload Your Code Files : "),sg.InputText(key="-inp-",size=(40, 1),enable_events=True),
                        sg.FilesBrowse(button_text="browse",enable_events=True)],
                       [sg.Text("Requester mail-id :         "),sg.InputText(key="maili",size=(25, 1),enable_events=True)],
                       [sg.Button(button_text="Upload",key="-upl-",enable_events=True,button_color="green")],
                      ]

        mail_window = sg.Window("Share Your Code",layout=mail_layout)
        while True:
            even,val = mail_window.read()
            if even is sg.WIN_CLOSED:
                break
            if even == "-inp-":
                pass
            if even == "-upl-":
                if (val["-inp-"] != "" and val["-inp-"] is not None) and (val["maili"] != "" and val["maili"] is not None):
                    try:
                       send_mail.send_code_files(val["-inp-"],requester_mail=val["maili"])
                    except:
                        sg.popup_no_buttons("give proper mail-id", auto_close=True, no_titlebar=True,
                                            background_color="red", relative_location=(70, 70))
                    os.remove('D:\CodeSign_files_upload.zip')
                    sg.popup_no_buttons("Uploaded!", auto_close=True, no_titlebar=True,
                                        background_color="green", relative_location=(70, 70))
                else:
                    sg.popup_no_buttons("give proper details", auto_close=True, no_titlebar=True,
                                        background_color="red", relative_location=(70, 70))

    layout = [[sg.Text("")],
              [sg.Text("    Give Common Name*:    "),sg.Input(key="CN", size=(25, 1)),sg.Text("   Note :",font="Any 12",text_color="orange"),sg.Text("Add root to trust_store, Click here ->",text_color="orange",auto_size_text=True),sg.Button(button_text="Add",auto_size_button=True,button_color="grey",key="adtrust",enable_events=True)],
              [sg.Text("                                                     ",pad=((0,0),(15,0))),
               sg.Input(visible=False, key="tr", enable_events=True),
               sg.FolderBrowse(button_text="Request Certificate",key="-re-",auto_size_button=True,pad=((0,0),(15,15)))],
              [sg.Text("Note:",font="Any 13",text_color="red"),
               sg.Text(auto_size_text=True,text="You need to have signtool to sign your executable file with above provided certificate, \nIf you don't have any signtool kindly share your code file here (You will get signed file within 24 hrs by mail) :")],
              [sg.Text("                                                     "),
                         sg.Button(button_text="Share your code",button_color="green",auto_size_button=True,key="shar",pad=((0,0),(15,5))),
               sg.Exit(pad=((350,0),(15,5)),button_color="red")],
             ]
    wind1 = sg.Window(title="Code-Signing",layout=layout,icon=secu.icon_base64)

    while True:
        events,values = wind1.read()
        if events in ("Exit",sg.WIN_CLOSED):
            wind1.close();break
        if events == "adtrust":
            try:
                CAsigningcert.CAsigning.addtotrust()
            except:
                pass
        if events == "tr":
            path_to_save_pfx = values["-re-"]
            comm_name = values["CN"]
            try:
                gen_codesigncert(comm_name,path_to_save_pfx)
                sg.popup_no_buttons("Downloaded successfully", auto_close=True, no_titlebar=True,
                                background_color="green", relative_location=(70, 70))
            except:
                sg.popup_no_buttons("provide proper CN", auto_close=True, no_titlebar=True,
                                    background_color="red", relative_location=(70, 70))

        if events == "shar":
            mail_gui()
        wind1.refresh()


