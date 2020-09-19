import sys, fitz
from pathlib import Path
from natsort import natsorted
import os

def pdf(dir, num = 50 ):
    # Prepare image list
    path = "./"+dir
    imglist = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.png')]
    imglist = natsorted(imglist)

    # Number of files to join
    current_chap = ''

    # Start making pdf
    for i in range(0,int(len(imglist)/num) + 1):
        doc = fitz.open()                            # PDF with the pictures
        for j, f in enumerate(imglist[i*num:(i+1)*num]):
            try:
                img = fitz.open(f) # open pic as document
            except:
                break
            rect = img[0].rect                       # pic dimension
            pdfbytes = img.convertToPDF()            # make a PDF stream
            img.close()                              # no longer needed
            imgPDF = fitz.open("pdf", pdfbytes)      # open stream as PDF
            page = doc.newPage(width = rect.width,   # new page with ...
                               height = rect.height) # pic dimension
            page.showPDFpage(rect, imgPDF, 0)
                   # image fills the page
            current_chap = f.split("-")[-1].split(".")[-2]
            os.remove(f)
        file_name =  'Chapter '+current_chap+ '.pdf'
        doc.save(file_name)
        print("Done "+file_name)
        Path("./"+file_name).rename("./"+dir+"/"+file_name)
