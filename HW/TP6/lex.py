from ply import lex,yacc
import inputs

# 'COMMENT_BEGINNING',
# 'COMMENT_ENDING',
tokens = [
    'SINGLE_COMMENT',
    'MULTI_LINE_COMMENT',
    'FUNCTION_BEGINNING',
    'FUNCTION_ENDING',
    'LIST_BEGINNING',
    'LIST_ENDING',
    'LINE_ENDING',
    'ARG_BEGINNING',
    'ARG_ENDING',
    'STRING',
    'INT',
    'FLOAT',
    'SYMBOL',
    'EQUAL',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'BIGGER',
    'SMALLER',  
    'RANGE',
    'ARG_SEPERATOR'
]

# t_COMMENT_BEGINNING = r'\/\*'
# t_COMMENT_ENDING = r'\*\/'
t_MULTI_LINE_COMMENT = r'\/\*(.|\n)*\*\/'
t_SINGLE_COMMENT = r'\/\/[^\n]*'
t_FUNCTION_BEGINNING = r'\{'
t_FUNCTION_ENDING = r' \}'
t_LIST_BEGINNING = r'\['
t_LIST_ENDING = r'\]'
t_LINE_ENDING = r';'
t_ARG_BEGINNING = r'\('
t_ARG_ENDING = r'\)'
t_STRING = r'".*"'
t_SYMBOL = r'[a-zA-Z][\w\.]*'
t_EQUAL = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_BIGGER = r'>'
t_SMALLER = r'<'
t_RANGE = r'\.{2}'
t_ARG_SEPERATOR = r','
t_ignore = ' \n\t'
 

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Illegal Character: ",t)
    t.lexer.skip(1)

lexer = lex.lex()
lexer.input(inputs.exp2)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)



