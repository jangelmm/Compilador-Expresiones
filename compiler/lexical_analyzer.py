# compiler/lexical_analyzer.py

import re
from .symbol_tables import RESERVED_WORDS, OPERATORS, DELIMITERS, VariableSymbolTable

class LexicalAnalyzer:
    """
    Convierte una lista de lexemas en tokens usando tablas fijas y variables.
    """
    def __init__(self, lexemes, symbol_table=None):
        self.lexemes = lexemes
        self.tokens = []
        self.symbol_table = symbol_table if symbol_table is not None else VariableSymbolTable()

    def analyze(self):
        """Realiza el análisis y devuelve los tokens y el reporte."""
        self._tokenize()
        report = self._generate_markdown()
        return self.tokens, report

    def _tokenize(self):
        """Genera una lista de tokens a partir de la lista de lexemas."""
        for lexeme in self.lexemes:
            # Verificar si es palabra reservada
            if lexeme.upper() in RESERVED_WORDS:
                self.tokens.append(('RESERVED_WORD', lexeme, RESERVED_WORDS[lexeme.upper()]))
            # Verificar si es operador
            elif lexeme in OPERATORS:
                self.tokens.append(('OPERATOR', lexeme, OPERATORS[lexeme]))
            # Verificar si es delimitador
            elif lexeme in DELIMITERS:
                self.tokens.append(('DELIMITER', lexeme, DELIMITERS[lexeme]))
            # Verificar si es número entero
            elif lexeme.isdigit():
                self.tokens.append(('CONSTANT', lexeme, None))
                # Agregar a la tabla de símbolos si no existe
                if not self.symbol_table.find_symbol_by_name(lexeme):
                    self.symbol_table.add_symbol(lexeme, 'integer', value=lexeme)
            # Verificar si es identificador (comienza con letra o _)
            elif re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', lexeme):
                # Si no está en la tabla de símbolos, agregarlo
                if not self.symbol_table.find_symbol_by_name(lexeme):
                    self.symbol_table.add_symbol(lexeme, 'integer')  # Por defecto integer
                # Buscar el ID del símbolo
                symbol_id = None
                for sid, info in self.symbol_table.symbols.items():
                    if info['name'] == lexeme:
                        symbol_id = sid
                        break
                self.tokens.append(('IDENTIFIER', lexeme, symbol_id))
            else:
                # No se reconoce el lexema
                raise ValueError(f"Lexema no reconocido: '{lexeme}'")

    def _generate_markdown(self):
        md = "## 2. Análisis Lexicográfico\n\n"
        md += "El **análisis léxico** toma las palabras detectadas y las clasifica según su tipo.\n"
        md += "Para ello, el compilador compara cada lexema con **tablas de referencia**.\n\n"
        
        md += ">**Objetivo:**\n"
        md += "> Convertir la secuencia de caracteres en una **secuencia de tokens** (unidades mínimas con significado).\n\n"
        
        md += "---\n\n"
        md += "### Tablas consultadas\n\n"
        
        md += "#### a) Tabla fija (Palabras reservadas y operadores)\n\n"
        md += "| Código | Token | Tipo |\n"
        md += "|:------:|:-----:|:----:|\n"
        for word, code in RESERVED_WORDS.items():
            md += f"| {code} | `{word}` | palabra reservada |\n"
        for op, code in OPERATORS.items():
            md += f"| {code} | `{op}` | operador |\n"
        for delim, code in DELIMITERS.items():
            md += f"| {code} | `{delim}` | delimitador |\n"
        
        md += "\n#### b) Tabla variable (Identificadores y constantes)\n\n"
        md += "| Posición | Lexema | Tipo | Valor |\n"
        md += "|:--------:|:------:|:----:|:-----:|\n"
        for symbol_id, info in self.symbol_table.symbols.items():
            md += f"| {symbol_id} | `{info['name']}` | {info['type']} | {info.get('value', '—')} |\n"
        
        md += "\n---\n\n"
        md += "### Tokens generados\n\n"
        md += "| Tipo | Valor |\n"
        md += "|:-----|:-----:|\n"
        for kind, value, _ in self.tokens:
            md += f"| {kind} | `{value}` |\n"
        
        md += "\n---\n\n"
        md += "### Resultado del análisis léxico:\n\n"
        md += "Una lista de **tokens** identificados y clasificados, sin errores.\n"
        md += "Si existiera una palabra desconocida, el compilador la reportaría como **símbolo no reconocido**.\n\n"
        md += "---\n"
        
        return md