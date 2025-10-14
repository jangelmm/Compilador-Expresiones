# compiler/lexical_analyzer.py

import re
from .symbol_tables import RESERVED_WORDS, OPERATORS, DELIMITERS, VariableSymbolTable

class LexicalAnalyzer:
    """
    Convierte una cadena de código fuente en tokens usando tablas fijas y variables.
    """
    TOKEN_SPECIFICATIONS = [
        ('KEYWORD_VAR',         r'\bvar\b'),
        ('KEYWORD_PROC',        r'\bproc\b'),
        ('KEYWORD_BEGIN',       r'\bbegin\b'),
        ('KEYWORD_END',         r'\bend\b'),
        ('TIPO_DATO',           r'\b(integer|char|real)\b'),
        ('STRING',              r"'[^']*'"),  # Strings entre comillas simples
        ('ID',                  r'[a-zA-Z_]\w*'),
        ('NUMERO_REAL',         r'\d+\.\d*|\.\d+'),  # Números reales (1.23, .5, 3.)
        ('NUMERO_ENTERO',       r'\d+'),
        ('OPERADOR_ASIGNACION', r':='),
        ('OPERADOR_ARITMETICO', r'[+\-*/]'),
        ('OPERADOR_COMPARACION', r'[<>]=?|='),  # <, >, <=, >=, =
        ('OPERADOR_DESIGUALDAD', r'<>'),        # <>
        ('OPERADOR_LOGICO',     r'\b(and|or|not)\b'),  # ACTUALIZADO: agregar 'not'
        ('DELIMITADOR',         r'[:;]'),
        ('PAREN',               r'[()]'),
        ('SKIP',                r'[ \t\r\n]+'),
        ('MISMATCH',            r'.'),
    ]

    TOKEN_REGEX = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATIONS)

    def __init__(self, code_string, symbol_table=None):
        self.code = code_string
        self.tokens = []
        self.symbol_table = symbol_table if symbol_table is not None else VariableSymbolTable()

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
                raise ValueError(f"Caracter no reconocido: '{value}'")
            
            # Procesar según el tipo de token
            if kind in ['KEYWORD_VAR', 'KEYWORD_PROC', 'KEYWORD_BEGIN', 'KEYWORD_END', 'TIPO_DATO']:
                value = value.lower()
                token_id = RESERVED_WORDS.get(value)
                self.tokens.append(('RESERVED_WORD', value, token_id))
            
            elif kind in ['OPERADOR_ASIGNACION', 'OPERADOR_ARITMETICO', 'OPERADOR_COMPARACION', 'OPERADOR_DESIGUALDAD']:
                token_id = OPERATORS.get(value)
                self.tokens.append(('OPERATOR', value, token_id))

            elif kind == 'OPERADOR_LOGICO':  # Manejar operadores lógicos
                token_id = OPERATORS.get(value)
                self.tokens.append(('OPERATOR', value, token_id))

            elif kind == 'DELIMITADOR':
                token_id = DELIMITERS.get(value)
                self.tokens.append(('DELIMITER', value, token_id))

            elif kind == 'PAREN':
                self.tokens.append(('PAREN', value, None))

            elif kind == 'NUMERO_ENTERO':
                self.tokens.append(('CONSTANT', value, None))

            elif kind == 'NUMERO_REAL':
                self.tokens.append(('CONSTANT', value, None))

            elif kind == 'STRING':
                self.tokens.append(('STRING', value, None))

            elif kind == 'ID':
                # Verificar si el símbolo ya existe en la tabla
                symbol_exists = False
                for symbol_id, symbol_info in self.symbol_table.symbols.items():
                    if symbol_info['name'] == value:
                        symbol_exists = True
                        break
                
                if not symbol_exists:
                    # Solo agregar si no existe, usando tipo por defecto
                    symbol_type = 'integer'
                    self.symbol_table.add_symbol(value, symbol_type)
                
                # Buscar el ID del símbolo (ya sea existente o nuevo)
                symbol_id = None
                for sid, info in self.symbol_table.symbols.items():
                    if info['name'] == value:
                        symbol_id = sid
                        break
                
                self.tokens.append(('IDENTIFIER', value, symbol_id))

    def _generate_markdown(self):
        md = "## 1.1. Análisis Lexicográfico\n\n"
        md += "El código fuente se descompone en los siguientes tokens:\n\n"
        md += "| Tipo | Valor | ID |\n"
        md += "|------|-------|----|\n"
        for kind, value, token_id in self.tokens:
            md += f"| {kind} | `{value}` | {token_id} |\n"
        return md