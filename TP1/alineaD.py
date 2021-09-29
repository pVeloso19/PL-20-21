import re

def normal(name):#nome normalizado
    name = re.sub(u"[àáâãäå]", 'a', name)
    name = re.sub(u"[èéêë]", 'e', name)
    name = re.sub(u"[ìíîï]", 'i', name)
    name = re.sub(u"[òóôõö]", 'o', name)
    name = re.sub(u"[ùúûü]", 'u', name)
    name = re.sub(u"[ýÿ]", 'y', name)
    name = re.sub(u"[ß]", 'ss', name)
    name = re.sub(u"[ñ]", 'n', name)
    name = re.sub(r'[^\w' + r' \-\.\,' + r']', '', name)#remove simbolos excepto -., e espaço
    return name

nomeInput = input('Insira o nome do Autor: ')

while not re.search(r'[a-zA-Z]+', nomeInput):
    print('Nome Inválido!')
    nomeInput = input('Insira o nome do Autor: ')

nome = normal(nomeInput)#remove symbolos do nome já normalizado(excepto espaço e -)

bib = open('exemplo-utf8.bib', encoding='utf-8')
colabs = {}

for line in bib:
        
    authorLine = re.search(r'author *={*', line.strip())

    if authorLine: #se estamos na subcategoria de autor
        fimAuthors = False

        while not fimAuthors:
            endFound = re.search(r'}*,', line.strip()) #verificar se encontrou o fim da linha
            
            if endFound: #encontrou fim da linha
                fimAuthors = True

                deleteEnter = re.sub(r'\n', ' ', line.strip()) #apagar enter(quando nome vem em duas linhas separadas)
                deleteEndingLine = re.sub(r'\"*\{*\}*,$', '', deleteEnter.strip()) #apagar cenas no fim da linha
                deleteBeginningLine = re.sub(r' *author* *= *{*\"* *', '', deleteEndingLine) #apagar cenas no início da linha
                fixedLine = re.sub(r' +', ' ', deleteBeginningLine) #quando houver mais que um espaço é como se fosse um

                diferentAuthors = fixedLine.split(' and') #necessario assim mas problema com nomes ao contrario(ainda tem espaços)
                
                authors = []#lista sem os espaços iniciais e finais e com nomes na ordem correta

                for author in diferentAuthors:

                    normalAuthor = normal(author)#remove symbolos do nome já normalizado(excepto espaço, - e .)
                    newAuthor = normalAuthor.strip()

                    if ',' in newAuthor: #se for do tipo onde primeiro vem o ultimo nome
                        
                        duplo = newAuthor.split(',')
                        firstName = duplo[1].strip()
                        lastName = duplo[0].strip()
                        
                        corretAuthor = firstName + ' ' + lastName
                        authors.append(corretAuthor)
                    
                    else:
                        authors.append(newAuthor)

                dividedName = nome.split(' ')

                for name in authors: #verificar se autor que queremos está nessa linha

                    normalizedName = normal(name)
                    
                    expression = r'^(?i:' + dividedName[0][0] + r').*(' + dividedName[0][1:] + r')?( ?)'
                    lastWord = len(dividedName) - 1
                    counter = 1

                    while counter <= lastWord:

                        if counter<lastWord:
                            expression += r'(?i:' + dividedName[counter][0] + r')?(.?)(' + dividedName[counter][1:] + r')?( ?)'
                            counter+=1
                        else:
                            expression += r'(?i:' + dividedName[counter] + r')$'
                            break 
                    
                    sameAuthor = re.search(expression, normalizedName)
                    
                    if sameAuthor:# o autor está nessa linha(para todos os tipos de acrónimos)

                        for author in authors:
                            
                            normalizedAuthor = normal(author)

                            expression = r'^(?i:' + dividedName[0][0] + r').*(' + dividedName[0][1:] + r')?( ?)'
                            lastWord = len(dividedName) - 1
                            counter = 1

                            while counter <= lastWord:

                                if counter<lastWord:
                                    expression += r'(?i:' + dividedName[counter][0] + r')?(.?)(' + dividedName[counter][1:] + r')?( ?)'
                                    counter+=1
                                else:
                                    expression += r'(?i:' + dividedName[counter] + r')$'
                                    break 
                    
                            isOurAuthor = re.search(expression, normalizedAuthor)            

                            if isOurAuthor:#como é o autor não o adicionamos ao dicionário
                                pass

                            else:#é autor colaborador
                                 
                                if normalizedAuthor in colabs:
                                    colabs[normalizedAuthor] += 1
                                else:
                                    colabs[normalizedAuthor] = 1
                        
                        break #sai procurar na linha da linha
                    
                    else:
                        pass

            else: #não encontrou o fim
                nextLine = next(bib)
                line = line + nextLine #ir concatenado linhas
    
    else:
        pass


bib.close()

for key, value in list(colabs.items()):
    if key == '':
        colabs.pop(key, None)#retirar os campos vazios(importante)


orderedColabs = sorted(colabs.items())
loopedColabs = sorted(colabs.items())

for key1, value1 in orderedColabs:

    div1 = key1.split(' ')

    expression = r'^(?i:' + div1[0][0] + r').*(' + div1[0][1:] + r')?( ?)'
    lastWord = len(div1) - 1
    counter = 1

    while counter <= lastWord:

        if counter<lastWord:
            expression += r'(?i:' + div1[counter][0] + r')?(.?)(' + div1[counter][1:] + r')?( ?)'
            counter+=1
        else:
            expression += r'(?i:' + div1[counter] + r')$'
            break 

    for key2, value2 in loopedColabs:       
                
        match = re.search(expression, key2)

        if match:  
            
            div2 = key2.split(' ')

            if len(div1) > len(div2) and colabs[key2] > 0 and colabs[key1] > 0:
                colabs[key1] += colabs[key2]#palavra maior fica com os valores da menor
                colabs[key2] -= colabs[key2] + 1#colocar como -1 para sabermos que é para remover
            else:
                if len(div1) == len(div2):
                    if len(key1) > len(key2) and colabs[key2] > 0 and colabs[key1] > 0:
                        colabs[key1] += colabs[key2]#palavra maior fica com os valores da menor
                        colabs[key2] -= colabs[key2] + 1#colocar como -1 para sabermos que é para remover
                    else:
                        if len(key1) < len(key2) and colabs[key1] > 0 and colabs[key2] > 0:
                            colabs[key2] += colabs[key1]#palavra maior fica com os valores da menor
                            colabs[key1] -= colabs[key1] + 1#colocar como -1 para sabermos que é para remover
                        else:
                            if (key1 != key2) and colabs[key2] > 0 and colabs[key1] > 0:
                                colabs[key1] += colabs[key2]#palavra maior fica com os valores da menor
                                colabs[key2] -= colabs[key2] + 1#colocar como -1 para sabermos que é para remover
                else:
                    if len(div1) < len(div2) and colabs[key1] > 0 and colabs[key2] > 0:
                        colabs[key2] += colabs[key1]#palavra maior fica com os valores da menor
                        colabs[key1] -= colabs[key1] + 1#colocar como -1 para sabermos que é para remover


for key, value in sorted(colabs.items()):
    if value == -1:
        colabs.pop(key, value)

dotFile = open(nome + '.dot', "w")
dotFile.write("digraph G {")

for key, value in sorted(colabs.items()):
        dotFile.write('\"' + nome + '\" -> \"' + key + '\"[label=\"' + str(value) + '\"];')
        
dotFile.write("}")
dotFile.close()
