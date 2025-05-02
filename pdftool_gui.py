import PySimpleGUI as Psg, functions as fu

Psg.theme('Light Brown4')
layout = [
    [Psg.Text("Select a file:"), Psg.Input(key="-FOLDER-PATH", size=(70,1)), Psg.FolderBrowse()],
    [Psg.Column([[]], key="-CONTAINER-", justification="left")],  # Empty container to hold new elements
    [Psg.Button("Submit", size=(7,1)),Psg.Button("Merge PDFs", key="MERGE"), Psg.Button("Mass Print", key="PRINT")]

]


window = Psg.Window('Waterp Renaming Tool', layout,element_justification="c")
window.finalize() # Added this line
while True:
    event, values = window.read()
    if event == Psg.WINDOW_CLOSED : break

    if event == "Submit":
        folder = values["-FOLDER-PATH"]
        if not folder : continue
        print(f"Folder: {folder}")

        existing_elements = window["-CONTAINER-"].Widget.winfo_children()  # Get all elements in container
        for widget in existing_elements:
            widget.destroy()  # Remove all widgets in the container

        progress_bar_layout = fu.build_progress_bar(Psg, folder)
        window.extend_layout(window["-CONTAINER-"], progress_bar_layout)
        window["-CONTAINER-"].update(visible=True)  # Show container again
        window.refresh()  # Refresh UI to apply changes
        window.TKroot.update_idletasks()

        progress_bar = window["-PROG-"]  # Re-fetch the new progress bar
        progress_label = window["-PROG_LABEL-"]

        fu.process_files_in_folder(folder, progress_bar, progress_label, window)

    if event == "MERGE":
        folder = values["-FOLDER-PATH"]
        fu.merge_files(folder)


    if event == "PRINT":
        print("⚠️This button is here to test new functions")


window.close()