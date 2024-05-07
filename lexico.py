class AnalizadorLexico:
    def _init_(self):
        # Definir las expresiones regulares
        self.palabras_reservadas = set(['main', 'then', 'if', 'else', 'end', 'do', 'while', 'repeat', 'until', 'cin', 'cout', 'real', 'int', 'integer', 'boolean', 'true', 'false', 'float'])
        self.simbolos_especiales = {'(': 'PAR_IZQ', ')': 'PAR_DER', '{': 'LLAVE_IZQ', '}': 'LLAVE_DER', ';': 'PUNTO_COMA', ',': 'COMA'}
        self.operadores_aritmeticos = {'+': 'SUMA', '-': 'RESTA', '*': 'MULTIPLICACION', '/': 'DIVISION', '=': 'ASIGNACION'}
        self.operadores_relacionales = {'==': 'IGUALDAD', '!=': 'DIFERENTE', '<>': 'DIFERENTE2', '<': 'MENOR_QUE', '>': 'MAYOR_QUE', '<=': 'MENOR_IGUAL_QUE', '>=': 'MAYOR_IGUAL_QUE'}
        self.operadores_logicos = {'&&': 'AND', '||': 'OR', '!': 'NOT'}
        self.operadores_dobles = {'++': 'INCREMENTO', '--': 'DECREMENTO'}
        self.tokens = []
        self.errors = []

    # Método para realizar el análisis léxico
    def analizar(self, texto):
        resultados = []

        # Reiniciar la lista de errores
        self.errors = []

        # Comenzar el análisis caracter por caracter
        linea = 1
        col = 1
        i = 0
        while i < len(texto):
            if texto[i].isspace():
                if texto[i] == "\n":
                    linea += 1
                    col = 1
                else:
                    col += 1
                i += 1
                continue

            # Identificar comentarios de una línea
            if texto[i:i + 2] == "//":
                i = texto.find("\n", i)
                if i == -1:
                    break
                linea += 1
                col = 1
                continue

            # Identificar comentarios multilinea
            elif texto[i:i + 2] == "/*":
                end_comment_index = texto.find("*/", i)
                if end_comment_index == -1:
                    self.errors.append(f"Error léxico: comentario sin cerrar en línea {linea}")
                    break  # Salir del bucle si no se encuentra el cierre del comentario
                else:
                    linea += texto[i:end_comment_index].count("\n")
                    i = end_comment_index + 2
                    continue

            # Identificar palabras reservadas, identificadores y números
            if texto[i].isalpha():
                j = i + 1
                while j < len(texto) and (texto[j].isalnum() or texto[j] == "_"):
                    j += 1
                token = texto[i:j]
                if token in self.palabras_reservadas:
                    resultados.append(("PALABRA RESERVADA", linea, col, token))
                else:
                    resultados.append(("IDENTIFICADOR", linea, col, token))
                col += j - i
                i = j
                continue
            elif texto[i].isdigit():
                tiene_punto = False
                j = i + 1
                while j < len(texto) and (texto[j].isdigit() or (texto[j] == '.' and not tiene_punto)):
                    if texto[j] == '.':
                        tiene_punto = True
                    j += 1
                if tiene_punto and texto[j-1] == '.':
                    self.errors.append(f"Error léxico: formato incorrecto para número flotante en la línea {linea}, columna {col}")
                else:
                    if tiene_punto:
                        resultados.append(("NÚMERO FLOTANTE", linea, col, texto[i:j],))
                    else:
                        resultados.append(("NÚMERO ENTERO", linea, col, texto[i:j]))
                col += j - i
                i = j
                continue

            # Identificar símbolos especiales
            if texto[i] in self.simbolos_especiales:
                resultados.append((texto[i], self.simbolos_especiales[texto[i]], linea, col))
                i += 1
                col += 1
                continue

            # Identificar operadores aritméticos y relacionales
            if texto[i:i + 2] in self.operadores_relacionales:
                resultados.append((texto[i:i + 2], self.operadores_relacionales[texto[i:i + 2]], linea, col))
                i += 2
                col += 2
                continue
            elif texto[i] in self.operadores_relacionales:
                resultados.append((texto[i], self.operadores_relacionales[texto[i]], linea, col))
                i += 1
                continue

            # Identificar operadores lógicos
            if texto[i:i + 2] in self.operadores_logicos:
                resultados.append((texto[i:i + 2], self.operadores_logicos[texto[i:i + 2]], linea, col))
                i += 2
                col += 2
                continue
            elif texto[i] in self.operadores_logicos:
                resultados.append((texto[i], self.operadores_logicos[texto[i]], linea, col))
                i += 1
                continue

            if texto[i:i + 2] in self.operadores_dobles:
                resultados.append((texto[i:i + 2], self.operadores_dobles[texto[i:i + 2]], linea, col))
                i += 2
                col += 1
                continue
            elif texto[i] in self.operadores_aritmeticos:
                resultados.append((texto[i], self.operadores_aritmeticos[texto[i]], linea, col))
                i += 1
                col += 1
                continue

            self.errors.append(f"Error léxico: token no reconocido '{texto[i]}' en la línea {linea}, columna {col}")
            i += 1
            col += 1

        return resultados
