import PySimpleGUI as psg, functions as fu
import time

psg.theme('Light Brown4')
layout = [
    [psg.Text("Select a file:"), psg.Input(key="-FOLDER-PATH"), psg.FolderBrowse(),psg.Button("Submit", size=(7,1))],
    [psg.Column([[]], key="-CONTAINER-", justification="left")]  # Empty container to hold new elements
]


window = psg.Window('My Application', layout,element_justification="c")
window.finalize() # Added this line
while True:
    event, values = window.read()
    if event == psg.WINDOW_CLOSED : break

    if event == "Submit":
        folder = values["-FOLDER-PATH"]
        if not folder : continue
        print(f"Folder: {folder}")

        existing_elements = window["-CONTAINER-"].Widget.winfo_children()  # Get all elements in container
        for widget in existing_elements:
            widget.destroy()  # Remove all widgets in the container

        progress_bar_layout = fu.build_progress_bar(psg, folder)
        window.extend_layout(window["-CONTAINER-"], progress_bar_layout)
        window["-CONTAINER-"].update(visible=True)  # Show container again
        window.refresh()  # Refresh UI to apply changes
        window.TKroot.update_idletasks()  # Added this


        progress_bar = window["-PROG-"]  # Re-fetch the new progress bar
        progress_label = window["-PROG_LABEL-"]

        fu.process_files_in_folder(folder, progress_bar, progress_label, window)
window.close()
