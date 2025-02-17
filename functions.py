from fileinput import filename
from importlib.resources import read_text

import pdfplumber,glob
def get_file_download_url(file_name):
    extension =''
    if file_name==1:return
    try:
        download_url = file_name
        return download_url
    except Exception as e:
        print(f"An error occurred: {e}")


def list_files(dir_path):
    files =  glob.glob(dir_path+"/*.pdf")
    fileList = []
    for file in files:
        file_name = file.split("\\")[len(file.split("\\"))-1]
        fileList.append(file_name)
    return fileList


    #
    # pdffile = pdfplumber.open("C:\\Users\\star1\\OneDrive\\Bureau\\IAM BT\\0a3c0a77-c9de-4b12-834a-81ef45f49d50.pdf")
    # page = pdffile.pages[0]
    # text = page.extract_text()
    # invoice = text.split(" ")
    #
    # start = invoice.index("Electricité")
    #
    # chunk = invoice[start:start + 3]
    # in_number = chunk[len(chunk) - 1]
    # print(in_number)
    #
    #
    #
    #

# def extract_invoice(filename, invoice_type):
#     invoice_number = 0
#     return [filename, invoice_number]
# def find_duplicates(array):
#     return [filename]







pdffile = pdfplumber.open("C:\\Users\\star1\\OneDrive\\Bureau\\IAM BT\\0a3c0a77-c9de-4b12-834a-81ef45f49d50.pdf")
page = pdffile.pages[0]
text = page.extract_text()
invoice =  text.split(" ")

start = invoice.index("Electricité")

chunk = invoice[start:start + 3]
in_number = chunk[len(chunk) - 1]
print(in_number)