# compiler/lexical_analyzer.py

import re
from .symbol_tables import RESERVED_WORDS, OPERATORS, DELIMITERS

class LexicalAnalyzer:
    """
    Convierte una cadena de código fuente en tokens usando las tablas fijas y variables.
    """

    # En lexical_analyzer.py, actualizar TOKEN_SPECIFICATIONS:
    TOKEN_SPECIFICATIONS = [
        ('RESERVED_WORD',    r'\b(var|proc|begin|end|integer|char|real|program|boolean|string)\b'),
        ('OPERATOR',         r':=|[+\-*/]|[<>]=?|<>|\b(and|or|not)\b'),
        ('DELIMITER',        r'[;]'),  # Solo punto y coma como delimitador de sentencias
        ('COLON',            r':'),    # Separar los dos puntos
        ('COMMA',            r','),    # Separar las comas
        ('PAREN',            r'[()]'),
        ('DOT',              r'\.'),
        ('STRING',           r"'[^']*'"),
        ('NUMBER_REAL',      r'\d+\.\d*|\.\d+'),
        ('NUMBER_INTEGER',   r'\d+'),
        ('IDENTIFIER',       r'[a-zA-Z_]\w*'),
        ('SKIP',             r'[ \t\r\n]+'),
        ('MISMATCH',         r'.'),
    ]

    TOKEN_REGEX = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATIONS)

    def __init__(self, code_string, symbol_table):
        self.code = code_string
        self.symbol_table = symbol_table
        self.tokens = []
        self.program_name = None  # Nuevo: almacenar el nombre del programa

    def analyze(self):
        """Realiza el análisis léxico y devuelve los tokens y el reporte."""
        self._tokenize()
        report = self._generate_markdown()
        return self.tokens, report

    def _tokenize(self):
        """Genera tokens usando las tablas fijas y variables."""
        lines = self.code.split('\n')
        in_program_declaration = False
        
        for line in lines:
            # Buscar declaración de programa para extraer el nombre
            program_match = re.search(r'\bprogram\s+(\w+)\s*;', line, re.IGNORECASE)
            if program_match:
                self.program_name = program_match.group(1).lower()
                in_program_declaration = True
            
            # Tokenizar la línea
            for mo in re.finditer(self.TOKEN_REGEX, line, re.IGNORECASE):
                kind = mo.lastgroup
                value = mo.group()

                if kind == 'SKIP':
                    continue
                elif kind == 'MISMATCH':
                    raise ValueError(f"Carácter no reconocido: '{value}'")
                
                # Convertir a minúsculas solo para palabras reservadas e identificadores
                if kind in ['RESERVED_WORD', 'IDENTIFIER']:
                    value = value.lower()
                
                # Determinar el tipo de token usando las tablas
                token_info = self._classify_token(kind, value)
                self.tokens.append(token_info)
            
            # Resetear el flag después de procesar la línea con 'program'
            if in_program_declaration:
                in_program_declaration = False

    def _classify_token(self, kind, value):
        """
        Clasifica un token usando las tablas fijas y variables.
        Retorna: (tipo_token, lexema, id_tabla)
        """
        # 1. Primero buscar en tabla fija de palabras reservadas
        if kind == 'RESERVED_WORD':
            token_id = RESERVED_WORDS.get(value.lower())
            return ('RESERVED_WORD', value, token_id)
        
        # 2. Buscar en tabla de operadores
        elif kind == 'OPERATOR':
            token_id = OPERATORS.get(value)
            if token_id:
                return ('OPERATOR', value, token_id)
        
        # 3. Buscar en tabla de delimitadores
        elif kind == 'DELIMITER':
            token_id = DELIMITERS.get(value)
            if token_id:
                return ('DELIMITER', value, token_id)
        
        # 4. Dos puntos (para declaraciones de tipo)
        elif kind == 'COLON':
            return ('COLON', value, None)
        
        # 5. Coma (para separar variables)
        elif kind == 'COMMA':
            return ('COMMA', value, None)
        
        # 6. Punto (delimitador especial)
        elif kind == 'DOT':
            token_id = DELIMITERS.get(value)
            if token_id:
                return ('DELIMITER', value, token_id)
        
        # 7. Paréntesis
        elif kind == 'PAREN':
            return ('PAREN', value, None)
        
        # 8. Constantes numéricas
        elif kind in ['NUMBER_INTEGER', 'NUMBER_REAL']:
            return ('CONSTANT', value, None)
        
        # 9. Strings
        elif kind == 'STRING':
            return ('STRING', value, None)
        
        # 10. Identificadores - BUSCAR en tabla de símbolos variables
        elif kind == 'IDENTIFIER':
            # EXCEPCIÓN: Ignorar el nombre del programa
            if self.program_name and value.lower() == self.program_name:
                return ('PROGRAM_NAME', value, 'PROGRAM')
            
            # Buscar el símbolo en la tabla de variables
            symbol_id = None
            for sid, info in self.symbol_table.symbols.items():
                if info['name'] == value.lower():
                    symbol_id = sid
                    break
            
            if symbol_id is not None:
                return ('IDENTIFIER', value, symbol_id)
            else:
                # Variable no declarada - aún así creamos el token pero marcamos como no declarada
                return ('IDENTIFIER', value, 'UNDECLARED')
        
        # Si llegamos aquí, es un token no clasificado
        return ('UNKNOWN', value, None)

    def _generate_markdown(self):
        md = "## 1.1. Análisis Lexicográfico\n\n"
        md += "El código fuente se descompone en los siguientes tokens:\n\n"
        md += "| Token | Lexema | ID Tabla |\n"
        md += "|-------|--------|----------|\n"
        for token_type, lexema, table_id in self.tokens:
            md += f"| {token_type} | `{lexema}` | {table_id} |\n"
        return md