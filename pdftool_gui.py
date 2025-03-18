import PySimpleGUI as psg
psg.theme('Light Brown4')
layout = [
    [psg.Text("Select a file:"), psg.Input(key="-FOLDER-PATH"), psg.FolderBrowse(),psg.Button("Submit", size=(7,1))]

]

window = psg.Window('My Application', layout,element_justification="c")

while True:
    event, values = window.read()
    if event == psg.WINDOW_CLOSED:
        break
    if event == "Submit":
        folder = values["-FOLDER-PATH"]
        if folder == "":
            continue

        print(f"Folder: {folder}")
        print("============================================")
    window.close()
