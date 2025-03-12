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


def explore_folder(folder):
    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))  # Get all PDF files in the folder
    LEN = len(pdf_files)
    for file in pdf_files:
        print(f"Processing: {file}")  # Debugging line
        getfiledata(file)  # Call your function on each file
    return LEN



def getfiledata(file):
    fileData = {}
    pdf = pdfplumber.open(file)
    text = pdf.pages[0].extract_text().split(" ")
    pdf.close()
    val = ""
    for i in text:
        val += '\n{'+i+': ,'+ str(text.index(i))+'}'

    fileData['contrat_Waterp'] = text[text.index("Contrat")+3]
    fileData['contrat_SAP'] = text[text.index("Contrat")+1]
    fileData['facture'] = text[text.index("Electricité") + 2]
    fileData['N° Client'] = text[text.index("Client") + 1]
    index = next((i for i, v in enumerate(text) if "Adresse" in v), -1)
    client = text[text.index("Client") + 4:index]
    fileData['Nom Client'] =" ".join(client)

    rename_file(file,fileData['Nom Client']+" - " +fileData['facture'])
    print("#####################################")
    return fileData


#def list_files(dir_path):
    #files =  glob.glob(dir_path+"/*.pdf")
   # file_list = {}
   # duplicate_list = {}
   # with ThreadPoolExecutor (max_workers=20) as executor :
    #    results = executor.map(lambda file:(
    #                                 file.split("\\")[-1],
    #                                 pdfplumber.open(file).pages[0].extract_text().split(" ")[
    #                                pdfplumber.open(file).pages[0].extract_text().split(" ").index("Electricité")+2
     #                                ] if("Electricité") in pdfplumber.open(file).pages[0].extract_text().split(" ") else None
    #    ),files)
   # for result in results:
   #     if result and result[1]:
   #         file_list[result[0]] = result[1]
    #return file_list
    #
    #
    #
    # for file in files:
    #     file_page = pdfplumber.open(file).pages[0]
    #     text = file_page.extract_text()
    #     invoice = text.split(" ")
    #     if invoice.index("Electricité") < 0 : continue
    #     start = invoice.index("Electricité")
    #     chunk = invoice[start:start + 3]
    #     if len(chunk) < 3:
    #         print(f"Not enough words after 'Electricité' in {file}")
    #         continue
    #
    #     in_number = chunk[-1]
    #     file_name = file.split("\\")[-1]
    #     if in_number in file_list.values:
    #         duplicate_list [file_name] = in_number
    #     file_list[file_name] = in_number
    #
    # return duplicate_list
