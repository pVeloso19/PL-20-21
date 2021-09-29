import re

def sumValores(v):
    res = 0

    for val in v:
        res = res + float(val)
    
    return res

def maxValores(v):
    res = -9999999999999999999

    for val in v:
        val = float(val)
        if(val > res):
            res = val
    
    return res

def minValores(v):
    res = 9999999999999999999

    for val in v:
        val = float(val)
        if(val < res):
            res = val
    
    return res


f = open('exemploP4_3.csv', encoding='utf-8')

line = f.readline()

cabecalho = re.split(r';',line)

print('{')

i = 0
for line in f:

    if(i != 0):
        print('\t},')
        print('')

    i = i + 1

    sublinha = re.split(r';',line)
    print('\t{')
    for fazer in cabecalho:
        ultimo = False
        
        val = sublinha[cabecalho.index(fazer)]

        if(re.search(r'\n',val)):
            ultimo = True

        val = val.strip()

        if(m := re.search(r'([^*]+) *\* *(.*)',fazer)):
            # Se entrou aqui tem de ser uma lista de numeros | mas tira as aspas caso os numeros estejam entre aspas
            val = re.sub(r'"', r'', val)
            # Retira o nome do campo
            nome = m.group(1).strip()
            if(m.group(2)):
                faz = m.group(2)
                
                #elimina os parenteses referentes á lista
                val = re.sub(r'^\( *',r'',val)
                val = re.sub(r' *\)$',r'',val)
                valores = re.split(r',',val)

                if(faz == 'sum'):
                    # calcula a soma dos valores
                    valSum = sumValores(valores)
                    if(ultimo):
                        print(f'\t\t"{nome}" : {valSum}')
                    else:
                        print(f'\t\t"{nome}" : {valSum},')
                elif(faz == 'avg'):
                    # calcula a media dos valores
                    valAvg = sumValores(valores) / len(valores)
                    if(ultimo):
                        print(f'\t\t"{nome}" : {valAvg}')
                    else:
                        print(f'\t\t"{nome}" : {valAvg},')
                elif(faz == 'max'):
                    # calcula o maximo dos valores
                    valMax = maxValores(valores)
                    if(ultimo):
                        print(f'\t\t"{nome}" : {valMax}')
                    else:
                        print(f'\t\t"{nome}" : {valMax},')
                elif(faz == 'min'):
                    # calcula o minimo dos valores
                    valMin = minValores(valores)
                    if(ultimo):
                        print(f'\t\t"{nome}" : {valMin}')
                    else:
                        print(f'\t\t"{nome}" : {valMin},')
            else:
                # lista normal
                val = re.sub(r'^\(', r'[', val)
                val = re.sub(r'\)$', r']', val)
                
                #Tira espaços entre elementos da lista
                val = re.sub(r'^\[ *', r'[', val)
                val = re.sub(r' *]$', r']', val)
                val = re.sub(r' *, *', r',', val)

                #Se é uma lista de strings mete as aspas | elimina aspas no meio para evitar erros de abrir e fechar a string
                if(re.search(r'[^0-9\[\]\,]',val)):
                    val = re.sub(r'"', r'', val)
                    val = re.sub(r'^(\[)(.)', r'\1"\2', val)
                    val = re.sub(r'(.),', r'\1","', val)
                    val = re.sub(r'(.)]$', r'\1"]', val)

                if(ultimo):
                    print(f'\t\t"{nome}" : {val}')
                else:
                    print(f'\t\t"{nome}" : {val},')
        else:
            # não é lista | elimina aspas no meio para evitar erros de abrir e fechar a string
            val = re.sub(r'"', r'', val)
            if(ultimo):
                print(f'\t\t"{fazer.strip()}" : "{val}"')
            else:
                print(f'\t\t"{fazer.strip()}" : "{val}",')         

print('\t}')
print('')

print('}')

f.close()