import ply.yacc as yacc

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
    p.parser.variaveis[p[2]] = x
    res = "PUSHI 0\n"
    p[0] = res

#def p_declaracaoExpATR(p):
    #"Declaracao : INTDECL ID '<' '-' expressao ';' "


# Declarar uma lista
#def p_declaracaoListATR(p):
    #"Declaracao : LINTDECL ID '<' '-' Lista ';' "

def p_declaracaoList(p):
    "Declaracao : LINTDECL ID '[' INT ']' ';' "
    x = p.parser.numVar
    p.parser.numVar += p[4] 
    p.parser.variaveis[p[2]] = x

    p[0] = f'PUSHN {p[4]}\n'


# Zona de instrucoes
def p_zonaInstrucoesVazia(p):
    "ZonaInstrucoes : "
    p[0] = ""

def p_zonaInstrucoesNotVazia(p):
    "ZonaInstrucoes : Instrucoes"
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
    pos = p.parser.variaveis[p[1]]
    s1 = ""
    for token in p[4]:
        s1 += token
    p[0] = s1 + f'STOREG {pos}\n'

def p_AtribuicaoListEXP(p):
    "Instrucao : ID '[' expressao ']' '<' '-' expressao ';' "
    pos = p.parser.variaveis[p[1]]
    p[0] = 'PUSHGP\n' + f'PUSHI {pos}\n' + 'PADD\n' + p[3] + p[7] +'STOREN\n'


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
        print(f'ERROR. Variavel não declarada: {p[3]}.')
        p.parser.sucesso = False
    else:
        pos = p.parser.variaveis[p[3]]
        res = 'READ\n' + 'ATOI\n' + f'STOREG {pos}\n'

    p[0] = res


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
    p[0] = 'PUSHI 1\n' + p[1] + p[3] + 'EQUAL\n' + 'SUB\n'


#operacoes matematicas
def p_expressao(p):
    "expressao : fator"
    p[0] = p[1]

def p_expressao_plus(p):
    "expressao : fator '+' expressao"
    p[0] = p[1] + p[3] + 'ADD\n'

def p_expressao_menos(p):
    "expressao : fator '-' expressao"
    p[0] = p[1] + p[3] + 'SUB\n'

def p_termo_vezes(p):
    "expressao : fator '*' expressao"
    p[0] = p[1] + p[3] + 'MUL\n'

def p_termo_resto(p):
    "expressao : fator '%' expressao"
    p[0] = p[1] + p[3] + 'MOD\n'

def p_termo_div(p):
    "expressao : fator '/' expressao"
    p[0] = p[1] + p[3] + 'DIV\n'


def p_fator1(p):
    "fator : INT"
    p[0] = f'PUSHI {p[1]}\n'

def p_fator2(p):
    "fator : ID"
    res = "\n"
    if(p[1] not in p.parser.variaveis):
        print(f'ERROR. Variavel não declarada: {p[1]}.')
        p.parser.sucesso = False
    else:
        pos = p.parser.variaveis[p[1]]
        res = f'PUSHG {pos}\n'

    p[0] = res

def p_fatorL(p):
    "fator : ID '[' expressao ']' "
    pos = p.parser.variaveis[p[1]]
    s1 = ""
    for token in p[3]:
        s1 += token
    p[0] = 'PUSHGP\n' + f'PUSHI {pos}\n' + 'PADD\n' + s1 + 'LOADN\n'

def p_fatorExp(p):
    "fator : '(' expressao ')'"
    p[0] = p[2]

# error
def p_error(p):
    #p.parser.sucesso = False
    print('Syntax error ',p)


#####################################################################################################################################

parser = yacc.yacc()

parser.inst = 0
parser.numVar = 0
parser.variaveis = {}
parser.sucesso = True

import sys
param = sys.argv[1:]

f = open('erros.txt', encoding='UTF-8')
r = f.read()
#while(True):
 #   line = input('-> ')
  #  if(line == ''):
   #     break
   # r = r + '\n' + line

res = parser.parse(r)

if(parser.sucesso):
    print(res)