import re

f = open('exemplo-utf8.bib', encoding='utf-8')

temp = {}

for line in f:
    y = re.search(r'^\@[^{]+{([^,]+),',line.strip())
    if(y):
        res = ''
        dentro = True
        chave = ''
        temp2 = {}
        while(dentro):
            subline = f.readline()
            if(re.search(r'^}$',subline.strip())):
                dentro = False
            else:
                if(pal := re.search(r'([^="]+) *= *("|{|[0-9])?(.*)',subline)):
                    chave = pal.group(1).strip()

                    if(chave in temp2):
                        if(pal.group(2)):
                            temp2[chave] = temp2[chave] + ' ' + pal.group(2).strip()
                            if(pal.group(3)):
                                temp2[chave] = temp2[chave] + pal.group(3).strip()
                    else:
                        if(pal.group(2)):
                            temp2[chave] = pal.group(2).strip()
                            if(pal.group(3)):
                                temp2[chave] = temp2[chave] + pal.group(3).strip()
                else:
                    if(chave in temp2):
                        temp2[chave] = temp2[chave]+ ' ' + subline.strip()
                    else:
                        temp2[chave] = subline.strip()
                    
        temp[y.group(1)] = temp2

f.close()

json = open("alineaC.json", "w", encoding='utf-8')

json.write('{\n')

i = 1
ultimo = len(temp)
for (x,y) in temp.items():
    json.write(f'\t"{x}" : '+'{' + '\n')

    j = 1
    ultimo2 = len(y)
    for (s,v) in y.items():
        
        lista = False
        if((s == 'author' or s == 'editor') and not re.match(r'^{{',v.strip())):
            lista = True

        frase = re.sub(r'\\[^{]+{',r'',v.strip())
        frase = re.sub(r'{',r'',frase.strip())
        frase = re.sub(r',$',r'',frase.strip())
        frase = re.sub(r'}',r'',frase.strip())
        frase = re.sub(r'"',r'',frase.strip())
        frase = re.sub(r'\\',r'',frase.strip())

        number = False
        if(re.search(r'^[0-9]+$',frase.strip())):
            frase = re.sub(r'^0+$',r'0',frase.strip())
            frase = re.sub(r'^0+([1-9]+)',r'\1',frase.strip())
            number = True
        
        if(lista):
            frase = re.sub(r' and ',r'","',frase.strip())
            frase = '["'+ frase + '"]'
        else:
            if(not number):
                frase = '"' + frase + '"'
        
        if(j == ultimo2):
            json.write('\t\t"' + s + '"' +' : '+ frase + '\n')
        else:
            json.write('\t\t"' + s + '"' +' : '+ frase + ',' + '\n')
        
        j = j +1

    if(i == ultimo):
        json.write('\t}' + '\n')
    else:
        json.write('\t},' + '\n')

    json.write('' + '\n')

    i = i + 1

json.write('}' + '\n')

json.close()

print('Conversão Concluida!')