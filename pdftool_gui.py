import PySimpleGUI as psg, PySimpleGUI as sg
psg.theme('Light Brown4')
layout = [
    [psg.Text("Select a file:"), psg.Input(key="-FOLDER-PATH"), psg.FolderBrowse()],
    [psg.Button("Submit", size=(15,1)),psg.Button("Exit",size=(15,1))]
]

window = psg.Window('My Application', layout,element_justification="c")

while True:
    event, values = window.read()
    if event in (psg.WINDOW_CLOSED, 'Exit'):
        break
    if event == "Submit":
        folder = values["-FOLDER-PATH"]

        print(f"Folder: {folder}")
        print("============================================")
    window.close()
