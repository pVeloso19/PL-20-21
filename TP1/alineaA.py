import re

bib = open('exemplo-utf8.bib', encoding='utf-8')

categorias = {
    "@article" : 0,
    "@book" : 0,
    "@inBook" : 0,
    "@misc" : 0,
    "@online" : 0,
    "@inCollection" : 0,
    "@proceedings" : 0,
    "@inProceedings" : 0,
    "@mastersthesis" : 0,
    "@phdthesis" : 0,
    "@techreport" : 0,
    "@booklet" : 0,
    "@manual" : 0,
    "@unpublished" : 0
}

for line in bib:

    categoriaMatch = re.search(r'@[a-zA-Z]+', line)

    if categoriaMatch:
        categoria = categoriaMatch.group(0).lower()

        for key, value in categorias.items():            
            sameCategoria = re.search(r'(?i:' + categoria + r')', key)
            if sameCategoria and len(key) == len(categoria):
                categorias[key] += 1
    else:
        pass

bib.close()

html = open("alineaA.html", "w")

html.write('<!DOCTYPE html>')
html.write('<html>')
html.write('<head>')
html.write('<meta charset=\"utf-8\"')
html.write('</head>')
html.write('<body>')
html.write('<h1>Entradas por Categoria</h1>')
html.write('</body>')
html.write('<ul>')

for key, value in sorted(categorias.items()):
    html.write('<li>')
    html.write(key + ': ' + str(value))
    html.write('</li>')

html.write('</body>')
html.write('</html>')

html.close()