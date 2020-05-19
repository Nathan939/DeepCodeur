from yattag import Doc
import os
import xlrd

def htlm_generate():
    doc, tag, text = Doc().tagtext()

    doc.asis('<!DOCTYPE html>')
    with tag('html'):
        with tag('head'):
            doc.stag('link', rel="stylesheet", type="text/css", href="styleTest.css")
            with tag('title'):
                text('DeepCodeur')
        with tag('body'):
            with tag('h1'):
                text('Bonjour')
        #Récupération des données de Tableau.xlsx
    wb = xlrd.open_workbook(os.path.join(r'C:\xampp\htdocs\deepcodeurDJANGO\_Tests', 'Tableau.xlsx'))
    worksheet = wb.sheet_by_name('ListeHTML')
    doc, tag, text = Doc().tagtext()

    # Récuperation des données de document.py
    wb = xlrd.open_workbook(os.path.join(r'C:\xampp\htdocs\deepcodeurDJANGO\_Tests', 'document.py'))
    doc, tag, text = Doc().tagtext()


with open('resultat.txt') as f:
    myWords = [line.strip() for line in f]
    for wrd in myWords:
        for rowidx in range(worksheet.nrows):
            if worksheet.cell(rowidx, 0).value == wrd:
        if wrd in worksheet.col(0):


    if myWords.ok:
        print(worksheet.cell(rowidx, 1).value))

    
    

    f = open("indexTest.html", "w+")
    f.write(resultHTML)
    f.close()

    resultHTML = doc.getvalue()

    f = open("indexTest.html", "w+")
    f.write(resultHTML)
    f.close()

def css_generate():
    resultCSS = """
    h1{color:red;}
    body{font-family: Arial, sans-serif; font-style: italic;}"""

    f = open("styleTest.css", "w+")
    f.write(resultCSS)
    f.close()





if __name__ == "__main__":
    htlm_generate() + html_printer()
    css_generate()