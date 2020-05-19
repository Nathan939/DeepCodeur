from yattag import Doc

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
    htlm_generate()
    css_generate()