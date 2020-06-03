import document as dc

from yattag import Doc
from bs4 import BeautifulSoup as bs

doc, tag, text = Doc().tagtext()

doc.asis('<!DOCTYPE html>')
with tag('html'):
    with tag('head'):
        doc.stag('link', rel="stylesheet", type="text/css", href="styleTest.css")
        for el in dc.balises_all:
            if el.emplacement == "haut":
                with tag(el.balise, klass=el.style):
                    text(el.contenu)
    with tag('body'):
        for el in dc.balises_all:
            if el.emplacement == "milieu":
                with tag(el.balise, klass=el.style):
                    text(el.contenu)
    with tag('foot'):
        for el in dc.balises_all:
            if el.emplacement == "bas":
                with tag(el.balise, klass=el.style):
                    text(el.contenu)

soup = bs(doc.getvalue())
print(soup.prettify())

f = open("indexTest.html", "w+")
f.write(soup.prettify())
f.close()
