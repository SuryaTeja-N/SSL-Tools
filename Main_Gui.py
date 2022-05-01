import PySimpleGUI as sg
import CAsigningcert
import Generate as make
import CAsigningcert as sir
from zipfile import ZipFile
import os,GET_PFX,code_signing_test,Credentials as secu,send_mail
import conve

sg.theme('Reds')

test_txt = ""; provided_csr_window3 = ""

def requesting(csr_co:str):
    req_layout = [[sg.Text("Download Certificate", font="Any 12", pad=((90, 0), (0, 20)))],
                  [sg.Checkbox(text=".crt", key="crt"),
                   sg.Checkbox(text=".pem (with chain)", key="pem")],
                  [sg.Input(visible=False,key="tr",enable_events=True),
                   sg.FolderBrowse(button_text="Download",auto_size_button=True, key="savi", pad=((0, 40), (30, 0)), enable_events=True),
                   sg.Button(button_text="Share via mail", key="mail", pad=((10, 40), (30, 0)))
                      , sg.Exit(pad=((20, 0), (30, 0)), key="quit")]
                  ]
    min_window3 = sg.Window("Get signed certificate", req_layout, size=(350, 150),icon=secu.icon_base64)

    mail_layou1 = [[sg.Text(text="Enter recipient mail ids here:")],
                   [sg.Input(tooltip="for multiple ids separate with comma", key="mails", enable_events=True)],
                   [sg.Text(text="")],
                   [sg.Button(button_text="Share", key="shr", pad=((130, 0), (0, 0)))],
                   ]
    mail_windo = sg.Window(title="Sharing Certificate", layout=mail_layou1,icon=secu.icon_base64)
    while True:
        even, val = min_window3.read()
        if even in ("Exit", "quit", sg.WIN_CLOSED):
            break
        if even == "tr":
            ct = sir.CAsigning.createsig_cert(csr_co)
            pem_ct = ct + "\n" + bytes.fromhex(secu.main_cert).decode()
            if val["crt"] is True:
                open(val["savi"] + "\signed_certificate.crt", "w").write(ct)
            if val["pem"] is True:
                open(val["savi"] + "\pem_file.pem", "w").write(pem_ct)
            if (val["crt"] is False) and (val["pem"] is False):
                sg.popup_no_buttons("Kindly choose format", auto_close=True, no_titlebar=True,
                                    background_color="red", relative_location=(70, 43))
            if (val["crt"] is True) or (val["pem"] is True):
                sg.popup_no_buttons("Downloaded successfully", auto_close=True, no_titlebar=True,
                                    background_color="green", relative_location=(70, 43))
                break

        if even == "mail":
            ct = sir.CAsigning.createsig_cert(csr_co)
            pem_ct = ct + "\n" + bytes.fromhex(secu.main_cert).decode()
            if (val["crt"] is False) and (val["pem"] is False):
                sg.popup_error("you haven't selected any formate", no_titlebar=True, background_color="red",
                               auto_close=True)
            else:
                with ZipFile(r'D:\Certificates.zip', 'w') as myzip:
                    if val["crt"] is True:
                        open(r"D:\Cert_format.crt", "w").write(ct)
                        myzip.write(r"D:\Cert_format.crt")
                        os.remove(r"D:\Cert_format.crt")
                    if val["pem"] is True:
                        open(r"D:\Pem_with_chain.pem", "w").write(pem_ct)
                        myzip.write(r"D:\Pem_with_chain.pem")
                        os.remove(r"D:\Pem_with_chain.pem")
                while True:
                    ev, va = mail_windo.read()
                    if ev == sg.WIN_CLOSED:
                        break
                    if ev == "shr":
                        try:
                            send_mail.send_mail(r'D:\Certificates', va["mails"])
                            sg.popup_no_buttons("shared successfully", auto_close=True, no_titlebar=True,
                                                background_color="green", relative_location=(70, 70))
                        except:
                            sg.popup_no_buttons("Give proper mail ids", auto_close=True, no_titlebar=True,
                                                background_color="red",
                                                relative_location=(70, 70))
                        break
                    mail_windo.refresh()
                os.remove(r'D:\Certificates.zip')
                mail_windo.close()
        min_window3.refresh()
    min_window3.close()

def window_mini1():
    info = [sg.Frame("Info",layout=[
                [sg.Text("1. Private key will be generated in #PKCS8 (which will give leverage to protect with password)",auto_size_text=True)],
                [sg.Text("2. If you choose RSA and DSA algorithm, select key size above or equal to 1024",auto_size_text=True)],
                [sg.Text("3. key usage options will be added in future..😊")]
           ],element_justification="c",pad=((45,0),(0,10)))]

    layout1 = [
        [sg.Text('CSR Generator',font='Any 16',pad=((270,0),(0,20)))],
        [sg.Text('Fill the details to generate CSR',pad=((40,0),(10,20)),font='Any 11'),info],
        [sg.Text("Common Name*: ",pad=((40,0),(10,10))),sg.Input(key="CN",size=(19,1),pad=((38,0),(0,0)))],
        [sg.Text("Country Name: ",pad=((40,0),(10,10))),sg.Input(key="CoN",size=(19,1),pad=((50,0),(0,0)))],
        [sg.Text("Organization_name: ",pad=((40,0),(10,10))),sg.Input(key="Org",size=(19,1),pad=((20,0),(0,0)))],
        [sg.Text("mail id: ",pad=((40,0),(10,10))),sg.Input(key="mail",size=(19,1),pad=((95,0),(10,0)))],
        [sg.Text("Sub. Alt Names:",pad=((40,0),(10,10))),sg.Input(key="alt_names",size=(30,10),pad=((45,0),(10,0)),tooltip="separate with ; for multiple values")],
        [sg.Text('passphrase: ',pad=((40,0),(10,10))),
         sg.Input(password_char="*",size=(19,1),pad=((65,0),(0,0)),key="password",tooltip="Leave empty for unencrypted key")],
        [sg.Text("select Key Algorithm: ",pad=((40,0),(10,10))),
         sg.Combo(["rsa","ec","dsa"],default_value="rsa",key="algo",pad=((40,0),(0,10)))],
        [sg.Text("select key size: ",pad=((40,0),(10,10))),
         sg.Combo(["384","1024","2048","4096","5068"],default_value="2048",key="key-size",pad=((70,0),(0,0)),auto_size_text=True,enable_events=True)],
        [sg.Input(key="saves",visible=False,enable_events=True),
         sg.FolderBrowse(button_text="save",key="file_index",visible=True,pad=((40,0),(60,0)),),
         sg.Button(button_text="copy csr",auto_size_button=True,key="copy",pad=((200,0),(60,0)),enable_events=True),
         sg.Exit(auto_size_button=True,key="exit",button_color='red',pad=((300,0),(60,0)))
         ],
      ]

    window1 = sg.Window('CSR & Key', layout1,size=(700,650),grab_anywhere=True,icon=secu.icon_base64)
    while True:
        events,values = window1.read()
        if events == "saves":
            make.b.CSR_and_Private_Generate(algo=values["algo"],size=int(values["key-size"]),folder_path=values["file_index"],
                                                password=values["password"],cn=values["CN"],country=values["CoN"],
                                                org=values["Org"],mail_id=values["mail"],sub_alt=values["alt_names"],
                                                gen_csr=True,gen_key=True)

            sg.PopupQuickMessage("CSR & key generated 👍", auto_close_duration=2, background_color="#bba592",
                                 keep_on_top=True, non_blocking=True, line_width=70, text_color="#000000",
                                 relative_location=(50, 280))

        if events == "copy":
            make.b.CSR_and_Private_Generate(algo=values["algo"], size=int(values["key-size"]),
                                                folder_path=None,
                                                password=values["password"], cn=values["CN"], country=values["CoN"],
                                                org=values["Org"], mail_id=values["mail"], sub_alt=values["alt_names"],
                                                gen_key=False,gen_csr=False)

            sg.clipboard_set(make.b.csr_txt)

            sg.PopupQuickMessage("CSR copied 👍", auto_close_duration=2, background_color="#bba592",
                                 keep_on_top=True, non_blocking=True, line_width=70, text_color="#000000",
                                 relative_location=(50, 280))

        if events in ("exit",sg.WIN_CLOSED):
            break
        window1.refresh()
    window1.close()
            
def window_mini2():

    info = [sg.Frame("Info", layout=[
        [sg.Text("1. Generated certificate is self-signed (signed by its own private key)",
                 auto_size_text=True)],
        [sg.Text("2. Do not use for production purposes as it was not signed by any CA.",
                 auto_size_text=True)],
        [sg.Text("3. both server and client authentication enabled.")]
    ], element_justification="c", pad=((45, 0), (0, 10)))]

    layout2 = [
        [sg.Text('Self-Signed Certificate', font='Any 16', pad=((200, 0), (0, 20)))],
        [sg.Text('Fill the certificate details', pad=((40, 0), (10, 20)), font='Any 11'), info],
        [sg.Text("Common Name*: ", pad=((40, 0), (10, 10))), sg.Input(key="CN", size=(19, 1), pad=((38, 0), (0, 0)))],
        [sg.Text("Country Name: ", pad=((40, 0), (10, 10))), sg.Input(key="CoN", size=(19, 1), pad=((50, 0), (0, 0)))],
        [sg.Text("Organization_name: ", pad=((40, 0), (10, 10))),
         sg.Input(key="Org", size=(19, 1), pad=((20, 0), (0, 0)))],
        [sg.Text("mail id: ", pad=((40, 0), (10, 10))), sg.Input(key="mail", size=(19, 1), pad=((95, 0), (10, 0)))],
        [sg.Text("Sub. Alt Names:", pad=((40, 0), (10, 10))),
         sg.Input(key="alt_names", size=(30, 10), pad=((45, 0), (10, 0)),
                  tooltip="separate with ; for multiple values")],
        [sg.Text("select Key Algorithm: ", pad=((40, 0), (10, 10))),
         sg.Combo(values=["rsa","ec","ds"],default_value="rsa",auto_size_text=True,enable_events=True,key="alg",pad=((40,0),(7,10))),
         ],
        [sg.Input(key="saves", visible=False, enable_events=True),
         sg.SaveAs(button_text="save", key="file_index", visible=True, pad=((40, 0), (60, 0)),file_types=(("CRT Files","*.crt"),), ),
         sg.Exit(auto_size_button=True, key="exit", button_color='red', pad=((450, 0), (60, 0)))
         ],
    ]
    window1 = sg.Window('Self-signed certificate', layout2, size=(600, 550), grab_anywhere=True,icon=secu.icon_base64)
    while True:
        events, values = window1.read()
        if events == "saves":
            make.b.self_signed_cert(cn=values["CN"],country=values["CoN"],org=values["Org"],mail_id=values["mail"],
                                    alt_names=values["alt_names"],file_save=values["file_index"],algo=values["alg"])
            # sg.Window('Continue?', [[sg.T('Certificate is generated 👍')], [sg.Ok(s=10)]],
            #           disable_close=True).read(close=True)
            sg.PopupQuickMessage("certificate generated 👍",auto_close_duration=2,background_color="#bba592",
                                 keep_on_top=True,non_blocking=True,line_width=70,text_color="#000000",relative_location=(50,280))

        if events in ("exit", sg.WIN_CLOSED):
            break
    window1.close()

def script_val():
    layi = [[sg.Text("                                           "),
             sg.Text("Give your credentials",font="Any 12")],
            [sg.Text("")],[sg.Text("")],[sg.Text("Enter your ID:   "),sg.InputText(key="usr_id",size=(25, 1))],
            [[sg.Text("")]],[[sg.Text("")],sg.Text("Enter Password: "),sg.InputText(key="-passy-",password_char="#",size=(25, 1))],
            [sg.Text("")],[sg.Text("")],[sg.Text("")],[sg.Text("")],
            [sg.Button(button_text="Login",key="-chk-"),sg.Exit(pad=((450,0),(0,0)),button_color="red")]
            ]
    winf = sg.Window(title="Script validation",layout=layi,size=(550,350),icon=secu.icon_base64)
    while True:
        evei,vali = winf.read()
        if evei in (sg.WIN_CLOSED,"Exit"):
            winf.close();break
        if evei == "-chk-":
            if vali["usr_id"] != bytes.fromhex(secu.from_send).decode() or \
                    vali["-passy-"] != bytes.fromhex(secu.send_pass).decode():
                sg.popup_no_buttons("Invalid ID and password", auto_close=True, no_titlebar=True,
                                    background_color="red", relative_location=(70, 70))
            else:
                pass

def window_mini3():

    col1 = sg.Column([[sg.Text("Certificate Signed By CA",font="Any 16",pad=((340,0),(0,15)))],
                      [sg.Text("Upload CSR file:  "),sg.Input(key="-source-",enable_events=True)
                          ,sg.FileBrowse(file_types=(("Text Files", "*.txt"),("pem files","*.pem"))
                                         ,enable_events=True,key="source",target="-source-")],
                      [sg.Text(text="OR paste csr content below and click check: ")],
                      [sg.Multiline(tooltip="Paste CSR content here and Click check",size=(80,25)
                                    ,key="-cont-",auto_size_text=True,do_not_clear=True,auto_refresh=True)],
                      ])

    col2 = sg.Column([[sg.Frame("CSR details:",layout=[[sg.Multiline(size=(60,20),no_scrollbar=True,key="vali")]],pad=((0,0),(25,0)))]
                      ])

    col3 = sg.Column([[ sg.Text("")],
                       [sg.Text("Note: ",font="Any 13",text_color="red"),sg.Text("To recognize this certificate by windows, You need to add root cert to root-truststore by click  here: "),
                        sg.Button(button_text="Add Root",enable_events=True,auto_size_button=True,key="adtrust",button_color="grey")],
                       [sg.Button(button_text="check",auto_size_button=True,pad=((20,0),(25,0)),key="ch"),
                        sg.Button(button_text="Request Certificate",auto_size_button=True,pad=((360,0),(25,0)),key="req"),
                        sg.Exit(button_color="red",pad=((380,0),(25,0)))]
                      ])

    layout3 = [[col1,col2],[col3]]

    window3 = sg.Window("Sign by CA",layout3,size=(1000,650),icon=secu.icon_base64)
    while True:
        events,values = window3.read()
        if events == "-source-":
            con = open(values["source"],"r").read()
            global provided_csr_window3; provided_csr_window3 = con
            window3.find_element("-cont-").update(con)
            window3.find_element("ch").update(disabled=True)
            window3.find_element("vali").update(make.b.csr_valid(con)+"\n\n"+"This CSR  is   "+ make.b.csr_valid_test.capitalize())
        if events == "ch":
            con = values["-cont-"]
            provided_csr_window3 = con
            window3.find_element("vali").update(make.b.csr_valid(con)+"\n\n"+"This CSR  is   "+ make.b.csr_valid_test.capitalize())
        if events == "req":
            requesting(globals()["provided_csr_window3"])
        if events == "adtrust":
            try:
               CAsigningcert.CAsigning.addtotrust()
            except:
                pass
        if events in (sg.WIN_CLOSED,"Exit","quit"):
            break
        window3.refresh()
    window3.close()


def main_window():
    layout = [
        [sg.Text('SSL Tools',font='Any 16',pad=((270,0),(0,50)))],
        [sg.Button(button_text="CSR & Key",tooltip="Generate CSR along with private key",size=(20,10),key="-gen-",pad=((0,0),(0,0))),
         sg.Button(button_text="Self-signed crt",size=(20,10),key="-gen_self-",pad=((80,0),(0,0))),
         sg.Button(button_text="Sign CSR by CA",size=(20,10),key="send to ca",pad=((80,0),(0,0)))],
        [sg.Button(button_text="Get PFX from CA",tooltip="no need of CSR",size=(20,10),key="-pfx_sign-",pad=((0,0),(30,0))),
         sg.Button(button_text="Code Signing Cert",size=(20,10),key="-code_sgn-",pad=((80,0),(30,0))),
         sg.Button(button_text="Script Validator (beta)",size=(20,10),key="-scp-",pad=((80,0),(30,0)))],
        [sg.Button(button_text="file conversion",key="file_cov",pad=((10,130),(100,0))),
         sg.Exit(button_color="red",pad=((390,0),(100,0)))]
        ]

    window = sg.Window('Window 4', layout,size=(700,600),grab_anywhere=True,icon=secu.icon_base64)

    while True:
        events,values = window.read()
        if events == "-gen-":
            window_mini1()
        if events == "-gen_self-":
            window_mini2()
        if events == "send to ca":
            window_mini3()
        if events == "-pfx_sign-":
            GET_PFX.reqPFX_gui()
        if events == "-code_sgn-":
            code_signing_test.codesign_gui()
        if events == "-scp-":
            script_val()
        if events == "file_cov":
            conve.conve_ui_pfx()
        if events in ("Exit",sg.WIN_CLOSED):
            break
        window.refresh()
    window.close()

main_window()
#sg.theme_previewer(columns=8,scrollable=True)

