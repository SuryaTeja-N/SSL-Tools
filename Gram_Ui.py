import PySimpleGUI as sg
import Check_for_Gram

sg.theme('LightGreen'); outputtext = ""; mainwindow_outputfile=""

def in_window1():
    layout1 = [[sg.Text('Corrector', font='Any 15')],
               [sg.Frame('Your Text', font='Any 15', layout=[
                   [sg.Multiline(size=(65, 15),key="Input_Text",font='Courier 10')]]),
                sg.Frame('Corrected Text',key="Output", font='Any 15', layout=[
                   [sg.Output(size=(65, 15),key="output_text", font='Courier 10')]])],
               [sg.Button("Check",auto_size_button=True,pad=((535,0),(0,0))),
                sg.Button("Copy", auto_size_button=True, pad=((300,0), (0, 0))),
                sg.Button("Clear", auto_size_button=True, pad=((25,0), (0, 0))),
                sg.Button('Exit',button_color=('white','firebrick3'),pad=((105,0),(0,0)))]
               ]
    window1 = sg.Window('Side-by-Side Check',layout1,auto_size_text=True,
                        auto_size_buttons=True,resizable=True,grab_anywhere=True).finalize()

    while True:
        event,values = window1.read()
        if event == "Check":
            values["Output"] = str(Text_Check.make_correct(values["Input_Text"]))
            outputtext = str(values["Output"])
            window1.find_element("output_text").update(values["Output"])
        if event in ('Exit','Quit', sg.WIN_CLOSED):
            break
        if event == "Clear":
            window1.find_element("Input_Text").update("")
            window1.find_element("output_text").update(""); outputtext=""
        if event == "Copy":
            sg.clipboard_set(outputtext)
        window1.refresh()
    window1.close()

def main_window():
    layout = [[sg.Text('Corrector', font='Any 15',pad=((200,0),(0,0)))],
              [sg.Text('Upload Text File here:  ',pad=(0,0)), sg.Input(key='-sourcefile-', size=(45, 1),pad=((0,0),(0,0))),
               sg.FileBrowse(key="input_file",file_types=(("Text Files", "*.txt"),))],
              [sg.Button('Make Correction',auto_size_button=True)],
              [sg.Frame('Output', font='Any 15', layout=[
                  [sg.Output(key="out_content",size=(65, 15), font='Courier 10')]])],
              [sg.InputText(visible=False,enable_events=True,key="saving_file"),
               sg.FileSaveAs(button_text="save",file_types=(("Text Files", "*.txt"),)),
               sg.Button('or Click for side-by-side check.', bind_return_key=True,auto_size_button=True),
               sg.Button('Quit', button_color=('white', 'firebrick3'))]]

    window = sg.Window('Spell Checker', layout, auto_size_text=True, auto_size_buttons=True,
                       default_element_size=(20, 1),grab_anywhere=True,resizable=True).finalize()

    while True:
        event, values = window.read()
        if event == "Make Correction":
            values["out_content"] = Text_Check.make_correct(open(values["input_file"],"r").read())
            mainwindow_outputfile = str(values["out_content"])
            window.find_element("out_content").update(values["out_content"])

        if event == "saving_file":
            with open(values["saving_file"],"x") as file:
                file.write(mainwindow_outputfile)

        if event in ("Exit","Quit",sg.WIN_CLOSED):
            break

        if event == "or Click for side-by-side check.":
            in_window1()
    window.close()

main_window()

