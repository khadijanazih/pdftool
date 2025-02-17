import PySimpleGUI as psg

psg.theme("Dark Purple 3")

layout = [
    [psg.Text("Select a folder:"), psg.Input(key="-FOLDER-"), psg.FolderBrowse()],
    [psg.Text("Additional Component:"), psg.Input(key="-ADDITIONAL-")],
    [psg.Button("Submit"), psg.Button("Exit")]
]

window = psg.Window('My Application', layout, size=(715, 250))

while True:
    event, values = window.read()
    if event in (psg.WINDOW_CLOSED, 'Exit'):
        break
    if event == "Submit":
        folder = values["-FOLDER-"]

        # print(f"Folder: {folder}")
        print("============================================")
    window.close()
