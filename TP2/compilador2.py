import ply.yacc as yacc
import math

from compilador_lex import tokens

def p_programa(p):
    "programa : ZonaDeclaracao ZonaInstrucoes"
    p[0] = p[1] + 'START\n' + p[2] + 'STOP'


#Zona de declaracoes
def p_declaracao_vazia(p):
    "ZonaDeclaracao : "
    p[0] = ""

def p_declaracao_notvazia(p):
    "ZonaDeclaracao : Declaracoes"
    p[0] = p[1]

def p_declaracoes_paragem(p):
    "Declaracoes : Declaracao"
    p[0] = p[1]

def p_declaracoes_rec(p):
    "Declaracoes : Declaracoes Declaracao"
    p[0] = p[1] + p[2]


#Declarar um inteiro
def p_declaracaoID(p):
    "Declaracao : INTDECL ID ';' "
    x = p.parser.numVar
    p.parser.numVar += 1 
    p.parser.variaveis[p[2]] = (x,'INT',[])
    res = "PUSHI 0\n"
    p[0] = res

def p_declaracaoList(p):
    "Declaracao : LINTDECL ID Array ';' "
    x = p.parser.numVar
    espaco = math.prod(p[3])
    p.parser.numVar += espaco 
    p.parser.variaveis[p[2]] = (x,'LINT',p[3])

    p[0] = f'PUSHN {espaco}\n'

def p_arraySingle(p):
    "Array : '[' INT ']'"
    p[0] = [p[2]]

def p_arrayNotSingle(p):
    "Array : Array '[' INT ']'"
    p[0] = p[1] + [p[3]]

# Zona de instrucoes
def p_zonaInstrucoesVazia(p):
    "ZonaInstrucoes : "
    p[0] = ""

def p_zonaInstrucoesNotVazia(p):
    "ZonaInstrucoes : Instrucoes"
    p.parser.temInst = True
    p[0] = p[1]

def p_InstrucoesParagem(p):
    "Instrucoes : Instrucao"
    p[0] = p[1]

def p_Instrucoes(p):
    "Instrucoes : Instrucoes Instrucao"
    p[0] = p[1] + p[2]


#Atribuicoes
def p_AtribuicaoInt(p):
    "Instrucao : ID '<' '-' expressao ';' "
    if(p[1] in p.parser.variaveis):
        (pos,tipo,ig2) = p.parser.variaveis[p[1]]
        if(tipo != 'INT'):
            print(f'WARNING: Atribuir valor a um array sem declarar a posição. A usar: {p[1]}[0]...')
        p[0] = p[4] + f'STOREG {pos}\n'
    else:
        print(f'ERRO: Variável "{p[1]}" não declarada.')
        p.parser.sucesso = False
        p[0] = "\n" 

def p_AtribuicaoListEXP(p):
    "Instrucao : ID ListArrayExp '<' '-' expressao ';' "
    if(p[1] in p.parser.variaveis):
        (pos,tipo,tam) = p.parser.variaveis[p[1]]
        
        if(tipo == 'LINT'):

            if(len(p[2]) == len(tam)):
                l = p[2]
                temp = ""
                
                if(len(l) != 1):
                    i = 0
                    while(i < (len(l)-1)):
                        temp += l[i] + f'PUSHI {tam[i]}\n' + 'MUL\n'
                        if((i+1)<((len(l)-1))):
                            i += 1
                            temp += l[i] + f'PUSHI {tam[i]}\n' + 'MUL\n' + 'ADD\n'
                        i += 1
                    temp += l[len(l)-1] + 'ADD\n'
                else:
                    temp = l[0]
                
                p[0] = 'PUSHGP\n' + f'PUSHI {pos}\n' + 'PADD\n' + temp + p[5] +'STOREN\n'
            else:
                print(f'ERRO: Variavel "{p[1]}" apenas contém {len(tam)} dimensões (contra as {len(p[2])} dimensões a usar)')
                p.parser.sucesso = False
                p[0] = "\n"            
        else:
            print('WARNING: Atribuição de índices a uma variável INT. IGNORANDO o índice.')
            p[0] = p[5] + f'STOREG {pos}\n'
    else:
        print(f'ERRO: Variável "{p[1]}" não declarada.')
        p.parser.sucesso = False
        p[0] = "\n" 

# IF
def p_InstrucaoIF(p):
    "Instrucao : SE '(' condicao ')' '{' if '}' "
    num = p.parser.inst
    p[0] = p[3] + f'JZ endIF{num}\n' + p[6] + f'endIF{num}: nop\n'
    p.parser.inst += 1

def p_InstrucaoIFElse(p):
    "Instrucao : SE '(' condicao ')' '{' if '}' '{' else '}' "
    num = p.parser.inst
    p[0] = p[3] + f'JZ else{num}\n' + p[6] + f'JUMP endIf{num}\n' + f'else{num}: nop\n' + p[9] + f'endIf{num}: nop\n'
    p.parser.inst += 1

def p_if(p):
    "if : ZonaInstrucoes"
    p[0] = p[1]

def p_else(p):
    "else : ZonaInstrucoes"
    p[0] = p[1]


#while
def p_InstrucaoENQUANTO(p):
    "Instrucao : ENQUANTO '(' condicao ')' '{' ciclo '}' "
    num = p.parser.inst
    p[0] = f'testa{num}: nop\n' + p[3] + f'JZ saiciclo{num}\n' + p[6] + f'JUMP testa{num}\n' + f'saiciclo{num}: nop\n'
    p.parser.inst += 1

def p_ciclo(p):
    "ciclo : ZonaInstrucoes"
    p[0] = p[1]


#Ler do input 
def p_InstrucaoLER(p):
    "Instrucao : LER '(' ID ')' ';' "
    res = "\n"
    if(p[3] not in p.parser.variaveis):
        print(f'ERRO: Variavel "{p[3]}" não declarada.')
        p.parser.sucesso = False
        p[0] = "\n" 
    else:
        (pos,tipo,ig2) = p.parser.variaveis[p[3]]
        if(tipo!='INT'):
            print(f'WARNING: Atribuir valor a um array sem declarar a posição. A usar: {p[3]}[0]...')
        res = 'READ\n' + 'ATOI\n' + f'STOREG {pos}\n'
    p[0] = res

def p_InstrucaoLERarray(p):
    "Instrucao : LER '(' ID ListArrayExp ')' ';' "
    
    if(p[3] in p.parser.variaveis):
        (pos,tipo,tam) = p.parser.variaveis[p[3]]
        
        if(tipo == 'LINT'):

            if(len(p[4]) == len(tam)):
                l = p[4]
                temp = ""
                
                if(len(l) != 1):
                    i = 0
                    while(i < (len(l)-1)):
                        temp += l[i] + f'PUSHI {tam[i]}\n' + 'MUL\n'
                        if((i+1)<((len(l)-1))):
                            i += 1
                            temp += l[i] + f'PUSHI {tam[i]}\n' + 'MUL\n' + 'ADD\n'
                        i += 1
                    temp += l[len(l)-1] + 'ADD\n'
                else:
                    temp = l[0]
                
                p[0] = 'PUSHGP\n' + f'PUSHI {pos}\n' + 'PADD\n' + temp + 'READ\n' + 'ATOI\n' +'STOREN\n'
            else:
                print(f'ERRO: Variável "{p[3]}" apenas contém {len(tam)} dimensões (contra as {len(p[4])} dimensões a usar)')
                p.parser.sucesso = False
                p[0] = "\n"            
        else:
            print('WARNING: Atribuição de índices a uma variável INT. IGNORANDO o índice.')
            p[0] = 'READ\n' + 'ATOI\n' + f'STOREG {pos}\n'
    else:
        print(f'ERRO: Variável "{p[3]}" não declarada.')
        p.parser.sucesso = False
        p[0] = "\n" 

#Escrever no output
def p_InstrucaoESCREVERExp(p):
    "Instrucao : ESCREVER '(' expressao ')' ';' "
    p[0] = p[3] + 'WRITEI\n'

def p_InstrucaoESCREVERS(p):
    "Instrucao : ESCREVER '(' STRING ')' ';' "
    p[0] = f'PUSHS {p[3]}\n' + 'WRITES\n'

def p_InstrucaoESCREVERSV(p):
    "Instrucao : ESCREVER '(' STRING ',' expressao ')' ';' "
    p[0] = f'PUSHS {p[3]}\n' + 'WRITES\n' + p[5] + 'WRITEI\n'

# Condicoes
def p_condicao_menor(p):
    "condicao : expressao '<' expressao"
    p[0] = p[1] + p[3] + 'INF\n'

def p_condicao_maior(p):
    "condicao : expressao '>' expressao"
    p[0] = p[1] + p[3] + 'SUP\n'

def p_condicao_menorI(p):
    "condicao : expressao '<' '=' expressao"
    p[0] = p[1] + p[4] + 'INFEQ\n'

def p_condicao_maiorI(p):
    "condicao : expressao '>' '=' expressao"
    p[0] = p[1] + p[4] + 'SUPEQ\n'

def p_condicao_igual(p):
    "condicao : expressao '=' expressao"
    p[0] = p[1] + p[3] + 'EQUAL\n'

def p_condicao_diff(p):
    "condicao : expressao '!' '=' expressao"
    p[0] = 'PUSHI 1\n' + p[1] + p[4] + 'EQUAL\n' + 'SUB\n'


#operacoes matematicas
def p_expressao_plus(p):
    "expressao : expressao '+' termo"
    p[0] = p[1] + p[3] + 'ADD\n'

def p_expressao_menos(p):
    "expressao : expressao '-' termo"
    p[0] = p[1] + p[3] + 'SUB\n'

def p_expressao(p):
    "expressao : termo"
    p[0] = p[1]

def p_termo_vezes(p):
    "termo : termo '*' fator"
    p[0] = p[1] + p[3] + 'MUL\n'

def p_termo_resto(p):
    "termo : termo '%' fator"
    p[0] = p[1] + p[3] + 'MOD\n'

def p_termo_div(p):
    "termo : termo '/' fator"
    p[0] = p[1] + p[3] + 'DIV\n'

def p_termo(p):
    "termo : fator"
    p[0] = p[1]

def p_fator1(p):
    "fator : INT"
    p[0] = f'PUSHI {p[1]}\n'

def p_fator2(p):
    "fator : ID"
    res = "\n"
    if(p[1] not in p.parser.variaveis):
        print(f'ERRO: Variavel "{p[1]}" não declarada.')
        p.parser.sucesso = False
        p[0] = "\n" 
    else:
        (pos,tipo,ig2) = p.parser.variaveis[p[1]]
        if(tipo!='INT'):
            print(f'WARNING: Atribuir valor a um array sem declarar a posição. A usar: {p[1]}[0]...')
        res = f'PUSHG {pos}\n'

    p[0] = res

def p_fatorL(p):
    "fator : ID ListArrayExp "
    if(p[1] in p.parser.variaveis):
        (pos,tipo,tam) = p.parser.variaveis[p[1]]
        
        if(tipo == 'LINT'):

            if(len(p[2]) == len(tam)):
                l = p[2]
                temp = ""
                
                if(len(l) != 1):
                    i = 0
                    while(i < (len(l)-1)):
                        temp += l[i] + f'PUSHI {tam[i]}\n' + 'MUL\n'
                        if((i+1)<((len(l)-1))):
                            i += 1
                            temp += l[i] + f'PUSHI {tam[i]}\n' + 'MUL\n' + 'ADD\n'
                        i += 1
                    temp += l[len(l)-1] + 'ADD\n'
                else:
                    temp = l[0]
                
                p[0] = 'PUSHGP\n' + f'PUSHI {pos}\n' + 'PADD\n' + temp + 'LOADN\n'
            else:
                print(f'ERRO: Variavel "{p[1]}" apenas contém {len(tam)} dimensões (contra as {len(p[2])} dimensões a usar)')
                p.parser.sucesso = False
                p[0] = "\n"           
        else:
            print('WARNING: Atribuição de índices a uma variável INT. IGNORANDO o índice.')
            res = f'PUSHG {pos}\n'
    else:
        print(f'ERRO: Variável "{p[1]}" não declarada.')
        p.parser.sucesso = False
        p[0] = "\n" 


def p_fatorExp(p):
    "fator : '(' expressao ')'"
    p[0] = p[2]

def p_ListArrayExpStop(p):
    "ListArrayExp : '[' expressao ']' "
    p[0] = [p[2]]

def p_ListArrayExp(p):
    "ListArrayExp : ListArrayExp '[' expressao ']' "
    p[0] = p[1] + [p[3]]

# error
def p_error(p):
    parser.sucesso = False
    print('ERRO: Syntax error -> ',p)


#####################################################################################################################################

parser = yacc.yacc()

parser.inst = 0
parser.numVar = 0
parser.variaveis = {}
parser.sucesso = True
parser.temInst = False

import sys
import re
param = sys.argv[1:]

if(len(param)!=0):
    fich = param[0]
    
    outList = re.split(r'\.',fich)
    outCount = 0
    outName = ""
    while(outCount < (len(outList)-1)):
        outName += outList[outCount] + '.'
        outCount += 1 
    outName = outName + 'vm'

    f = open(fich, encoding='UTF-8')
    r = f.read()
    res = parser.parse(r)
    f.close()

    if(len(parser.variaveis) == 0):
        print('WARNING: Não foram declaradas variaveis.')
    
    if(parser.temInst == False):
        print('WARNING: Não foram declaradas instruções para o programa.')

    if(parser.sucesso == False):
        pass
    else:
        output = open(outName,'w', encoding='UTF-8')
        output.write(res)
        output.close()
else:
    print('ERRO: Nenhum ficheiro introduzido.')
    pass
