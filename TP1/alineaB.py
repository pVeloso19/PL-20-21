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
                    chave = pal.group(1).strip().lower()

                    if(chave =='author' and chave in temp2 and pal.group(2) and pal.group(3)):
                        temp2[chave] = temp2[chave] + ' ' + pal.group(2).strip() + pal.group(3).strip()
                    else:
                        if(chave =='author' and pal.group(2) and pal.group(3)):
                            temp2[chave] = pal.group(2).strip() + pal.group(3).strip()
                else:
                    if(chave =='author' and chave in temp2):
                        temp2[chave] = temp2[chave]+ ' ' + subline.strip()
                    else:
                        if(chave =='author'):
                            temp2[chave] = subline.strip()
                    
        temp[y.group(1)] = temp2

f.close()

b = open("alineaB.txt", "w", encoding='utf-8')

for (x,y) in temp.items():
    frase = ''
    for (s,v) in y.items():
        
        lista = False
        if(not re.match(r'^{{',v.strip())):
            lista = True

        frase = re.sub(r'{',r'',v.strip())
        frase = re.sub(r',$',r'',frase.strip())
        frase = re.sub(r'}',r'',frase.strip())
        frase = re.sub(r'"',r'',frase.strip())
        frase = re.sub(r'\\',r'',frase.strip())
        
        if(lista):
            frase = re.sub(r' and ',r'","',frase.strip())
            frase = '["'+ frase + '"]'
        else:
            frase = '"' + frase + '"'
    
    b.write(x + ':'+ frase + '\n')

b.close()

print('Concluido!')
