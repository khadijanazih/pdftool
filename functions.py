import pdfplumber,glob, os, math, PyPDF2
from datetime import datetime

#Main Function
def process_files_in_folder(folder,progress_bar, prog_label,window):
    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))  # Get all PDF files in the folder
    total_files = len(pdf_files)

    if total_files == 0:
        prog_label.update("No PDF files found.")
        return folder

    progress_bar.update(0, total_files, visible=True) # Reset progress bar
    window.TKroot.update_idletasks()

    for i, file in enumerate(pdf_files, start=1):
        file_name = os.path.basename(file)

        if file_name.startswith("Merged") or any (file_name.startswith(flag) for flag in ["Blank", "Not Compatible"]): continue
        try:
            print(f"⚠️ Processing: {os.path.splitext(os.path.basename(file))[0]}")  # Debugging line
            print("*************************************************")
            get_file_data(file)  # Call function on each file

            progress_bar.update_bar(i, total_files)  # Update progress bar
            prog_label.update(f"{math.ceil((i / total_files) * 100)} %")
            window.TKroot.update_idletasks()

        except Exception as e:
            print(f"⚠️ Error processing {file_name}: {e}")

    prog_label.update(f"Done {total_files} Files")
    print(f"Done ! Processed {total_files} Files")

    return folder

#Extracting Function
def get_file_data(file):
    file_data = {}
    file_flag =''
    file_name = os.path.splitext(os.path.basename(file))[0]

    with pdfplumber.open(file) as pdf:
        text_lines = pdf.pages[0].extract_text().splitlines()

    if is_blank(file):file_flag ="Blank"
    elif not is_compatible(file):file_flag ="Not Compatible"

    if file_flag:
        if file_name.split(" - ")[0] != file_flag:
            new_name = f"{file_flag} - {file_name}"
            ##ident here
            rename_file(file, new_name)
        return None

    #Facture Basse Tension
    tension = file_type(file)
    if  tension == "BT":
        lineind, textind = locate_text(text_lines, "Facture")
        file_data['facture'] = text_lines[lineind].split()[textind + 3]

        lineind, textind = locate_text(text_lines, "N°")
        file_data['N° Client'] = text_lines[lineind].split()[textind + 2]

        lineind, textind = locate_text(text_lines, "Client")
        file_data['Nom Client'] = " ".join(text_lines[lineind + 1].split()[textind:-1])

        lineind, textind = locate_text(text_lines, "Contrat")
        file_data['contrat_SAP'] = text_lines[lineind].split()[textind + 1]
        file_data['contrat_Waterp'] = text_lines[lineind].split()[textind + 3]

        new_name = tension + " - " + file_data['facture'] + " - " + file_data['N° Client'] + " - " + file_data['Nom Client']
        rename_file(file, new_name)

    # Facture Moyenne Tension
    elif tension == "MT":

        lineind, textind = locate_text(text_lines, "N°")
        file_data['facture'] = text_lines[lineind].split()[textind + 1]

        lineind, textind = locate_text(text_lines, "Client")
        file_data['N° Client'] = text_lines[lineind].split()[textind + 2]

        file_data['Nom Client'] = text_lines[0]
        lineind, textind = locate_text(text_lines, "Contrat")

        file_data['contrat_SAP'] = text_lines[lineind].split()[textind + 2]
        file_data['contrat_Waterp'] = text_lines[lineind].split()[textind + 4]

        new_name = file_data['Nom Client'] + " - " + file_data['facture'] + " " + tension
        rename_file(file, new_name)

    else :
        print(f" Unknown file type for: {file_name}")
        return None

    return file_data

#Helper Functions
def is_compatible(file):
    with pdfplumber.open(file) as pdf_file:
        pdf_txt = pdf_file.pages[0].extract_text().splitlines()

    contrat = locate_text(pdf_txt,"Contrat")
    client = locate_text(pdf_txt,"Client")
    return contrat != (-1,-1) and client != (-1,-1)

def is_blank(file):
    file_size = os.path.getsize(file)
    blank_size = 21000
    pdf = pdfplumber.open(file)
    pdf_text = pdf.pages[0].extract_text()
    pdf.close()
    return file_size <= blank_size or len(pdf_text)<=10

def file_type(file):
    with pdfplumber.open(file) as pdf:
        text = pdf.pages[0].extract_text().split(" ")
    if any("Usage" in word for word in text): return "BT"
    if any("Tarif" in word for word in text): return "MT"

def rename_file(file, new_name):
    dirpath = os.path.dirname(file)
    basename = os.path.splitext(new_name)[0]
    target_path = os.path.join(dirpath, f"{basename}.pdf")
    counter = 1

    while os.path.exists(target_path):
        target_path = os.path.join(dirpath, f"{basename} ({counter}).pdf")
        counter+=1

    os.rename(file, target_path)

def locate_text(text_split_array, text):
    line_index = -1
    text_index = -1
    for line in text_split_array:
        if text in line:
            line_split = line.split(" ")
            line_index = text_split_array.index(line)
            text_index = line_split.index(text)
            break
    return line_index, text_index

def get_file_count(folder):
    return len(glob.glob(os.path.join(folder, "*.pdf")))  # Get all PDF files in the folder

def merge_files(folder):
    pdf_files = glob.glob(os.path.join(folder, "*.pdf"))
    pdf_writer = PyPDF2.PdfWriter()
    for pdf_path in pdf_files:
        filename = os.path.basename(pdf_path)  # Just the filename, e.g., "Merged-21h40.pdf_path"

        if filename.startswith("Merged"):continue

        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                pdf_writer.add_page(page)


    time_str = datetime.now().strftime("%Hh%M")  # Format: 21h40
    output_path = os.path.join(folder, f"Merged-{time_str}.pdf")

    with open(output_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

    print(f"Merged PDF saved as: {output_path}")


#Build Progress Bar --- needs fixes
def build_progress_bar(psg,folder):

    return [
        [psg.Text("Progress : "), psg.ProgressBar(max_value=get_file_count(folder), size=(45, 20), key="-PROG-"), psg.Text("% : ", key="-PROG_LABEL-", size =(12,1))]
    ]


#EXTRA
# def extract_name(folder):
#     pdf_files = glob.glob(os.path.join(folder, "*.pdf"))  # Get all PDF files in the folder
#     for i, file in enumerate(pdf_files, start=1):
#         file_name = os.path.basename(file).split("-")[1]
#         print(file_name)
