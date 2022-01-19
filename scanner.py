from ply.lex import lex

literals = ['+', '-', '*', '/', '%', '(', ')', '[', ']', '{', '}', '=', ';', ':', ',', '\'', '\"']

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'false': 'FALSE',
    'true': 'TRUE',
    'int': 'INT',
    'float': 'FLOAT',
    'bool': 'BOOL',
    'char': 'CHARTYPE',
    'string': 'STRINGTYPE',
    'void': 'VOID',
    'printf': 'PRINT'
}

tokens = [
    # ASSIGN OPERATORS
    'PLUSASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'PLUSPLUS',
    'MINUSMINUS',
    # RELATIONAL OPERATORS
    'LESSER_THAN',
    'GREATER_THAN',
    'LESSER_EQUAL',
    'GREATER_EQUAL',
    'NOT_EQUAL',
    'EQUAL',
    # OTHER
    'ID',
    'FLOATNUM',
    'INTNUM',
    'CHAR',
    'STRING',
] + list(reserved.values())


t_ignore = ' \t'
t_ignore_COMMENT = r'//.*'

t_PLUSASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'\/='
t_PLUSPLUS = r'\+\+'
t_MINUSMINUS = r'--'

t_LESSER_THAN = r'\<'
t_GREATER_THAN = r'\>'
t_LESSER_EQUAL = r'\<='
t_GREATER_EQUAL = r'\>='
t_NOT_EQUAL = r'\!='
t_EQUAL = r'\=='

t_CHAR = r'\'([a-zA-Z_0-9\W])\''
t_STRING = r'\"([^\\\n]|(\\.))*?\"'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_FLOATNUM(t):
    r'([0-9]*[\.][0-9]+|[0-9]+[\.][0-9]*)((E|e)(\+|-)?[0-9]+)?|([0-9]+)((E|e)(\+|-)?[0-9]+)'
    #  .0 cases       OR  0. cases     AND maybe exp notation OR int with exp notation
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("line %d: illegal character '%s'" % (t.lineno, t.value[0]))
    t.lexer.skip(1)


lexer = lex()

if __name__ == "__main__":
    lexer = lex()
    with open('file.c', 'r') as f:
        # lines = f.readlines()
        lexer.input(f.read())
        for token in lexer:
            print("line %d: %s(%s)" % (token.lineno, token.type, token.value))