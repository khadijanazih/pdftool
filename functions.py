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
    LEN = len(pdf_files)
    for file in pdf_files:
        print(f"Processing: {file}")  # Debugging line
        get_file_data(file)  # Call your function on each file
    return LEN

def get_file_data(file):
    fileData = {}
    pdf = pdfplumber.open(file)
    text = pdf.pages[0].extract_text().split(" ")
    pdf.close()
    new_name = ""

    if len(text) <=10:
        new_name ="blank"
        rename_file(file, new_name)
        return
    try:
        fileData['facture'] = text[text.index("Electricité") + 2]
    except ValueError:
        print("'N° facture' is not in the list")
        new_name ="not compatible"
        rename_file(file, new_name)
        return

    fileData['contrat_Waterp'] = text[text.index("Contrat")+3]
    fileData['contrat_SAP'] = text[text.index("Contrat")+1]
    fileData['N° Client'] = text[text.index("Client") + 1]
    index = next((i for i, v in enumerate(text) if "Adresse" in v), -1)
    client = text[text.index("Client") + 4:index]
    fileData['Nom Client'] =" ".join(client)
    new_name = fileData['Nom Client']+" - " +fileData['facture']
    rename_file(file, new_name)
    print("#####################################")
    return fileData

def get_invoice_type(file):
    return 0