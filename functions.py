import pdfplumber,glob, os,re,json
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

def process_files_in_folder(folder):
    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))  # Get all PDF files in the folder
    folder_count = len(pdf_files)
    for file in pdf_files:
        print(f"Processing: {file}")  # Debugging line
        process = get_file_data(file)  # Call your function on each file
        print(json.dumps(process, indent=4))
    return folder_count

def get_file_data(file):
    file_data = {}
    pdf = pdfplumber.open(file)
    text = pdf.pages[0].extract_text().splitlines()
    pdf.close()
    new_name = ""
    tension = ""
    if len(text) <=10:
        new_name ="blank"
        rename_file(file, new_name)
        return
    if file_type(file) == "BT":
        try:
            lineind, textind = locate_text(text, "Facture")
            file_data['facture'] = text[lineind].split()[textind + 3]
        except ValueError:
            print("'N° facture' is not in the list")
            new_name ="not compatible"
            rename_file(file, new_name)
            return
        tension = "BT"

        lineind, textind = locate_text(text, "Contrat")

        file_data['contrat_SAP'] = text[lineind].split()[textind + 1]
        file_data['contrat_Waterp'] = text[lineind].split()[textind + 3]

        lineind, textind = locate_text(text, "N°")
        file_data['N° Client'] = text[lineind].split()[textind + 2]

        lineind, textind = locate_text(text, "Client")
        file_data['Nom Client'] = " ".join(text[lineind+1].split()[textind:-1])

    elif file_type(file) == "MT":
        try:
            lineind, textind = locate_text(text, "N°")
            file_data['facture'] = text[lineind].split()[textind + 1]
        except ValueError:
            print("'N° facture' is not in the list")
            new_name ="not compatible"
            rename_file(file, new_name)
            return
        tension = "MT"
        file_data['Nom Client'] = text[0]
        lineind, textind = locate_text(text, "Contrat")
        file_data['contrat_SAP'] = text[lineind].split()[textind + 2]
        file_data['contrat_Waterp'] = text[lineind].split()[textind + 4]
        lineind, textind = locate_text(text, "Client")
        file_data['N° Client'] = text[lineind].split()[textind + 2]

    new_name = file_data['Nom Client'] + " - " + file_data['facture']+ " " + tension
    rename_file(file, new_name)
    print("#####################################")
    return file_data
def file_type(file):
    pdf = pdfplumber.open(file)
    text = pdf.pages[0].extract_text().split(" ")
    pdf.close()
    if next((i for i, v in enumerate(text) if "Usage" in v), -1)>=0:
        return "BT"
    if next((i for i, v in enumerate(text) if "Tarif" in v), -1)>=0:
        return "MT"
def process_mt(file):
    file_data = {}
    pdf = pdfplumber.open(file)
    text = pdf.pages[0].extract_text().splitlines()
    pdf.close()

    file_data['Nom Client'] = text[0]
    file_data['facture'] = text[3].split(" ")[1]
    file_data['contrat_Waterp'] = text[5].split(" ")[4]
    file_data['contrat_SAP'] = text[5].split(" ")[2]
    file_data['N° Client'] = text[8].split(" ")[2]
    return file_data

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

def test_function(folder):
    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))  # Get all PDF files in the folder
    for file in pdf_files:
        if pdf_files.index(file)==10:break
        text = pdfplumber.open(file).pages[0].extract_text().splitlines()
        print(f"##### Processing: {file.split("\\")[-1].split(".")[0]} #####: ")
        lineind, textind = locate_text(text, "Client")
        print()

        print("------------------------------------------------------------")
