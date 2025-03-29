import pdfplumber,glob, os,re,time, math

def process_files_in_folder(folder,progress_bar, prog_label,window):
    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))  # Get all PDF files in the folder
    total_files = get_file_count(folder)
    progress_bar.update(0, total_files, visible=True) # Reset progress bar
    window.TKroot.update_idletasks()


    for i, file in enumerate(pdf_files, start=1):
        print(f"Processing: {os.path.splitext(os.path.basename(file))[0]}")  # Debugging line
        print("*************************************************")
        get_file_data(file)  # Call your function on each file
        time.sleep(0.1)  # Simulate processing time
        progress_bar.update_bar(i, total_files)  # Update progress bar
        prog_label.update(f"{ math.ceil((i/total_files)*100)} %")
        window.TKroot.update_idletasks()
        time.sleep(0.01)  # Add a short delay

    print(f"Done ! Processed {total_files} Files")

    return folder

def get_file_data(file):
    file_data = {}
    pdf = pdfplumber.open(file)
    text = pdf.pages[0].extract_text().splitlines()
    pdf.close()
    new_name, tension = "", ""

    file_name = os.path.splitext(os.path.basename(file))[0]
    if is_blank(file):
        if file_name.split(" - ")[0] == "Blank": new_name = file_name
        else : new_name ="Blank - " + file_name
        rename_file(file, new_name)
        return None

    if not is_compatible(file):
        if file_name.split(" - ")[0] == "Not Compatible": new_name = file_name
        else : new_name ="Not Compatible - " + file_name
        rename_file(file, new_name)
        return None




    if file_type(file) == "BT":
        tension = "BT"

        lineind, textind = locate_text(text, "Facture")
        file_data['facture'] = text[lineind].split()[textind + 3]

        lineind, textind = locate_text(text, "N°")
        file_data['N° Client'] = text[lineind].split()[textind + 2]

        lineind, textind = locate_text(text, "Client")
        file_data['Nom Client'] = " ".join(text[lineind+1].split()[textind:-1])

        lineind, textind = locate_text(text, "Contrat")
        file_data['contrat_SAP'] = text[lineind].split()[textind + 1]
        file_data['contrat_Waterp'] = text[lineind].split()[textind + 3]


        new_name = file_data['Nom Client'] + " - " + file_data['facture'] + " " + tension
        rename_file(file, new_name)

    elif file_type(file) == "MT":

        tension = "MT"

        lineind, textind = locate_text(text, "N°")
        file_data['facture'] = text[lineind].split()[textind + 1]

        lineind, textind = locate_text(text, "Client")
        file_data['N° Client'] = text[lineind].split()[textind + 2]

        file_data['Nom Client'] = text[0]
        lineind, textind = locate_text(text, "Contrat")

        file_data['contrat_SAP'] = text[lineind].split()[textind + 2]
        file_data['contrat_Waterp'] = text[lineind].split()[textind + 4]

        new_name = file_data['Nom Client'] + " - " + file_data['facture'] + " " + tension
        rename_file(file, new_name)
    print("#####################################")
    return file_data

#Helper functions
def rename_file(file, new_name):
    dirpath = os.path.dirname(file)
    new_path = os.path.join(dirpath, new_name+".pdf")

    # Regex to detect existing numbered filenames
    pattern = re.compile(r"(.*) \((\d+)\)$")
    basename = os.path.splitext(new_path)[0]
    match = pattern.match(basename)
    if match:
        basename, counter = match.groups()
        counter = int(counter)  # Extract the number and convert to integer

    else: counter = 1  # No number present initially

    while os.path.exists(new_path):
        new_path=basename+" ("+str(counter)+").pdf"
        counter+=1

    os.rename(file, new_path)
def file_type(file):
    pdf = pdfplumber.open(file)
    text = pdf.pages[0].extract_text().split(" ")
    pdf.close()
    if next((i for i, v in enumerate(text) if "Usage" in v), -1)>=0:
        return "BT"
    if next((i for i, v in enumerate(text) if "Tarif" in v), -1)>=0:
        return "MT"
def locate_text(text_split_array, text):
    line_index = -1
    text_index = -1
    for line in text_split_array:
        line_split = line.split(" ")
        if text in line:
            line_index = text_split_array.index(line)
            text_index = line_split.index(text)
            break
    return line_index, text_index
def is_compatible(file):
    pdf_file = pdfplumber.open(file)
    pdf_txt = pdf_file.pages[0].extract_text().splitlines()
    pdf_file.close()

    contrat = locate_text(pdf_txt,"Contrat")
    client = locate_text(pdf_txt,"Client")
    if contrat != (-1,-1) and client != (-1,-1):return True
    return False
def is_blank(file):
    file_size = os.path.getsize(file)
    blank_size = 21000
    pdf = pdfplumber.open(file)
    pdf_text = pdf.pages[0].extract_text()
    pdf.close()
    return file_size <= blank_size or len(pdf_text)<=10
def get_file_count(folder):
    return len(glob.glob(os.path.join(folder, "*.pdf")))  # Get all PDF files in the folder


#Build Progress Bar
def build_progress_bar(psg,folder):

    return [
        [psg.Text("Progress : "), psg.ProgressBar(max_value=get_file_count(folder), size=(45, 20), key="-PROG-"), psg.Text("% : ", key="-PROG_LABEL-")]
    ]