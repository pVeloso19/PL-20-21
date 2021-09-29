import ply.lex as lex

tokens = [
    'INT',
    'ID',
    'STRING',
    'SE',
    'ENQUANTO',
    'LER',
    'ESCREVER',
    'INTDECL',
    'LINTDECL'
]

literals = ['+','/','*','-','(',')','[',']','=','{','}','.','<','>','%',';',',','!']

def t_SE(t):
    r'(?i:SE)'
    return t

t_INTDECL = r'(?i:INT)'

t_LINTDECL = r'(?i:LINT)'

t_ENQUANTO = r'(?i:ENQUANTO)'

t_LER = r'(?i:LER)'

t_ESCREVER = r'(?i:ESCREVER)'

t_ID = r'\w+'

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING(t): 
    r'"[^"]+"'
    return t

t_ignore = ' \n\t'

def t_error(t):
    print('Illegal character: ', t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
