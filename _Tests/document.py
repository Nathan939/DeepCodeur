import xlrd
from yattag import Doc

import os

wb = xlrd.open_workbook(os.path.join(r'C:\xampp\htdocs\deepcodeurDJANGO\_Tests', 'Tableau.xlsx'))
worksheet = wb.sheet_by_name('ListeHTML')

doc, tag, text = Doc().tagtext()

# attendue = str(input("Quel mot ?"))

doc.asis('<!DOCTYPE html>')

# Recherche dans le résultat de l'enregistrement les balises qui corespondent avec le fichier excel
with open('resultat.txt') as f:
    myWords = [line.strip() for line in f]
    for wrd in myWords:
        for rowidx in range(worksheet.nrows):
            if worksheet.cell(rowidx, 0).value == wrd:
                print("Oui, ", wrd, " est une balise : ", worksheet.cell(rowidx, 1), " ", rowidx)
        if wrd in worksheet.col(0):
            print("Est dans la liste", worksheet.col(0))
                


                

print("\n", doc.getvalue())