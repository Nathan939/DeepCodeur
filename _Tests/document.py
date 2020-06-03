class PageElement(object):

    def __init__(self, emplacement, balise, contenu, style=''):
        self.emplacement = emplacement
        self.balise = balise
        self.contenu = contenu
        self.style = style

import xlrd

wb = xlrd.open_workbook('Tableau.xlsx')
worksheet = wb.sheet_by_name('ListeHTML')

with open("resultat.txt") as f:
    lines = f.read()
    words = lines.split()

w_emplac = ["haut", "milieu", "bas"]

w_balises = []
for rowidx in range(worksheet.nrows):
    w_balises.append(worksheet.cell(rowidx, 0).value)

starting = []
last = 0
for w in words:
    if w.lower() in w_emplac:
        starting.append(words.index(w, last))
        last = words.index(w, last) + 1

balises_all = []

for ind in starting:
    start_wo = words[ind]
    end = (starting[starting.index(ind) + 1] if starting.index(ind) + 1 != len(starting) else len(words))

    bal_wo = words[ind + 1]   

    good_bal = ''
    for hotbal in range(worksheet.nrows):
        if worksheet.cell(hotbal, 0).value.lower() == bal_wo.lower():
            good_bal = (worksheet.cell(hotbal, 1).value.lower()).replace("<", "").replace(">", "")
            break

    st_styles = None
    for w in words[ind:end]:
        if w.lower() == ("style" or "styles"):
            st_styles = words.index(w, ind)
            break

    final_style = ' '.join(words[st_styles + 1:end]) if st_styles else ''

    contenue = ' '.join(words[ind + 2:st_styles]) if st_styles else ' '.join(words[ind + 2:end])

    balises_all.append(PageElement(emplacement=start_wo, balise=good_bal, contenu=contenue, style=final_style))