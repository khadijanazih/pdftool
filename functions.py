import pdfplumber,glob, os,re
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
        print(get_file_data(file))  # Call your function on each file
    return folder_count

def get_file_data(file):
    file_data = {}
    pdf = pdfplumber.open(file)
    text = pdf.pages[0].extract_text().splitlines()
    for val in text :print(f"{text.index(val)} # {val}")

    pdf.close()
    new_name = ""
    tension = ""
    if len(text) <=10:
        new_name ="blank"
        rename_file(file, new_name)
        return
    if file_type(file) == "BT":
        try:
            file_data['facture'] = text[10].split(" ")[3]
        except ValueError:
            print("'N° facture' is not in the list")
            new_name ="not compatible"
            rename_file(file, new_name)
            return
        tension = "BT"
        file_data['contrat_SAP'] = text[5].split(" ")[text[5].split(" ").index("Contrat") + 1]
        file_data['contrat_Waterp'] = text[5].split(" ")[text[5].split(" ").index("Contrat")+3]
        file_data['N° Client'] = text[1].split(" ")[2]
        file_data['Nom Client'] = " " .join(text[2].split()[1:-1])

    elif file_type(file):
        try:
            file_data['facture'] = text[3].split(" ")[1]
        except ValueError:
            print("'N° facture' is not in the list")
            new_name ="not compatible"
            rename_file(file, new_name)
            return
        tension = "MT"
        file_data['Nom Client'] = text[0]
        file_data['contrat_Waterp'] = text[5].split(" ")[4]
        file_data['contrat_SAP'] = text[5].split(" ")[2]
        file_data['N° Client'] = text[8].split(" ")[2]

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