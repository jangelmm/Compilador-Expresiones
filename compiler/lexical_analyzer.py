# compiler/lexical_analyzer.py

import re

class LexicalAnalyzer:
    """
    Convierte una cadena de código fuente en tokens y genera un reporte.
    Esta versión es más robusta y maneja un conjunto más amplio de tokens.
    """
    # Especificación de tokens usando expresiones regulares
    TOKEN_SPECIFICATIONS = [
        # Palabras clave y Tipos de Datos se deben buscar antes que los IDs genéricos
        ('KEYWORD_VAR',         r'\bvar\b'),
        ('KEYWORD_PROC',        r'\bproc\b'),
        ('KEYWORD_BEGIN',       r'\bbegin\b'),
        ('KEYWORD_END',         r'\bend\b'),
        ('TIPO_DATO',           r'\b(integer|char|real)\b'),
        # Identificadores (variables, nombres de procedimientos)
        ('ID',                  r'[a-zA-Z_]\w*'),
        # Literales y Operadores
        ('NUMERO_ENTERO',       r'\d+'),
        ('OPERADOR_ASIGNACION', r':='),
        ('OPERADOR_ARITMETICO', r'[+\-*/]'),
        # Delimitadores y otros símbolos
        ('DELIMITADOR',         r'[:;]'),
        ('PAREN',               r'[()]'),
        # Ignorar espacios en blanco y saltos de línea
        ('SKIP',                r'[ \t\r\n]+'),
        # Cualquier otro caracter es un error
        ('MISMATCH',            r'.'),
    ]

    # Compilamos la expresión regular maestra que une todas las especificaciones
    TOKEN_REGEX = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATIONS)

    def __init__(self, code_string):
        self.code = code_string
        self.tokens = []

    def analyze(self):
        """Realiza el análisis y devuelve los tokens y el reporte."""
        self._tokenize()
        report = self._generate_markdown()
        return self.tokens, report

    def _tokenize(self):
        """Genera una lista de tokens a partir del código fuente."""
        for mo in re.finditer(self.TOKEN_REGEX, self.code, re.IGNORECASE):
            kind = mo.lastgroup
            value = mo.group()

            if kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                # Podríamos querer saber la línea y columna en un lexer más avanzado
                raise ValueError(f"Caracter no reconocido: '{value}'")
            
            # El valor de las palabras clave y tipos es el propio token
            if kind in ['KEYWORD_VAR', 'KEYWORD_PROC', 'KEYWORD_BEGIN', 'KEYWORD_END', 'TIPO_DATO']:
                value = value.lower()

            self.tokens.append((kind, value))

    def _generate_markdown(self):
        md = "## 1.1. Análisis Lexicográfico\n\n"
        md += "El código fuente se descompone en los siguientes tokens:\n\n"
        md += "| Tipo                    | Valor         |\n"
        md += "|-------------------------|---------------|\n"
        for kind, value in self.tokens:
            md += f"| {kind:<23} | `{value}`      |\n"
        return md