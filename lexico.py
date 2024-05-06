import ply.lex as lex

resultado_lexema = []

tokens = (
    'ENTERO',
    'REAL',
    'PALABRA_RESERVADA',
    'OPERADOR_ARITMETICO',
    'OPERADOR_RELACIONAL',
    'OPERADOR_LOGICO',
    'SIMBOLO',
    'ASIGNACION',
    'IDENTIFICADOR',
    'COMENTARIO_UNILINEA',
    'COMENTARIO_MULTILINEA',
)

# Expresiones regulares para los tokens
t_OPERADOR_ARITMETICO = r'[\+\-\*/%^\+\-]{2}|[\+\-\*\/%\^]'
t_OPERADOR_RELACIONAL = r'[<>]=?|!=|=='
t_SIMBOLO = r'[()\{\},;]'
t_ASIGNACION = r'='

# Definiciones de token más complejas
def t_REAL(t):
    r'\b\d+\.\d+\b|\b\d+\.\b'
    if '.' in t.value:
        if t.value.count('.') > 1 or t.value.endswith('.'):
            estado = f"** Error léxico en la línea {t.lineno}, posición {t.lexpos}: Número real mal formado '{t.value}'."
            resultado_lexema.append(estado)
            return
    t.value = float(t.value)
    return t

def t_ENTERO(t):
    r'\b\d+\b'
    t.value = int(t.value)
    return t

def t_PALABRA_RESERVADA(t):
    r'\b(?:if|else|do|while|switch|case|integer|double|main|cin|cout|int)\b'
    return t

# Definir operadores lógicos como tokens individuales
def t_OPERADOR_LOGICO(t):
    r'and|or'
    return t

def t_IDENTIFICADOR(t):
    r'\w+(_\d\w)*'
    return t

def t_COMENTARIO_UNILINEA(t):
    r'//.*'
    return t

def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    return t

def t_ignore_ESPACIO(t):
    r'\s+'
    if('\n+'):
        t.lexer.lineno += t.value.count('\n')
    
def t_error(t):
    global resultado_lexema
    estado = f"posición {t.lexpos}: Carácter '{t.value[0]}' no válido."
    resultado_lexema.append(estado)
    t.lexer.skip(1)

# Construyendo el analizador léxico
analizador = lex.lex()

def analizar_texto(text):
    global resultado_lexema
    resultado_lexema = [] 
    tokens_reconocidos = []
    analizador.lineno = 1
    analizador.input(text)
    aux1 = 1
    aux2 = 0
    aux3 = 0
    while True:
        tok = analizador.token()
        if not tok:
            break 
        #tok.lineno
        valor_token = tok.value if isinstance(tok.value, str) else str(tok.value)
        if aux1 < tok.lineno:
            aux1 += 1
            aux2 = tok.lexpos
        if tok.type == 'COMENTARIO_MULTILINEA' and len(tok.value.split('\n')) > 1:
            token_info = f"Desde: ({tok.lineno + aux3}, {tok.lexpos - aux2}) " \
                        f"Hasta: ({tok.lineno + tok.value.count('\n') + aux3}, {len(tok.value.split('\n')[-1])}) " \
                        f"{tok.type}: {tok.value}"
            aux3 += tok.value.count('\n')
            aux2 = tok.lexpos + len(tok.value) - len(tok.value.split('\n')[-1])
        else:
            token_info = f"Desde: ({tok.lineno + aux3}, {tok.lexpos - aux2}) " \
                        f"Hasta: ({tok.lineno + aux3}, {tok.lexpos - aux2 + len(valor_token)}) " \
                        f"{tok.type}: {tok.value}"
        #print(token_info)
        tokens_reconocidos.append(token_info)
    return tokens_reconocidos, resultado_lexema



if __name__ == "__main__":
    codigo_fuente = input("Ingrese el código fuente: ")
    resultado_lexico = analizar_texto(codigo_fuente)
    print(resultado_lexico)
