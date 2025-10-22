# compiler/parser.py

class Parser:
    """
    Realiza el parseo (lectura de caracteres) del código fuente.
    Segmenta el flujo de caracteres en lexemas usando delimitadores.
    """
    def __init__(self, code_string):
        self.code = code_string
        self.characters = []
        self.lexemes = []

    def parse(self):
        """Realiza el parseo y devuelve la lista de lexemas."""
        # Guardar secuencia de caracteres
        self.characters = list(self.code)
        
        # Segmentar en lexemas usando delimitadores
        current_lexeme = ''
        i = 0
        while i < len(self.code):
            char = self.code[i]
            
            if char in [' ', ':', '=', '+', '-', '*', '/', '(', ')', ';']:
                # Si encontramos un delimitador, añadimos el lexema actual (si existe)
                if current_lexeme:
                    self.lexemes.append(current_lexeme)
                    current_lexeme = ''
                
                # Caso especial: operador de asignación ':=' 
                if char == ':' and i + 1 < len(self.code) and self.code[i + 1] == '=':
                    self.lexemes.append(':=')
                    i += 2  # Saltar el siguiente carácter '='
                    continue
                elif char != ' ':  # Los espacios no se incluyen como lexemas
                    self.lexemes.append(char)
                
                i += 1
            else:
                current_lexeme += char
                i += 1
        
        # Añadir el último lexema si existe
        if current_lexeme:
            self.lexemes.append(current_lexeme)
            
        return self.lexemes

    def generate_markdown(self):
        """Genera el reporte Markdown para la fase de parseo."""
        md = "## 1. Parseo (Lectura del código fuente)\n\n"
        md += "También llamado **análisis de entrada**, es el paso más bajo del compilador.\n"
        md += "El compilador **no recibe palabras**, sino una **secuencia de caracteres**.\n\n"
        
        md += "> **Objetivo:**\n"
        md += "> Identificar los **límites de las palabras** (tokens potenciales) usando **delimitadores** como espacios, comas, puntos y comas, o paréntesis.\n\n"
        
        md += "**Ejemplo:**\n\n"
        md += "```\n"
        md += f"{self.code}\n"
        md += "```\n\n"
        
        md += "El parser lee carácter por carácter:\n\n"
        md += "| Paso | Carácter |\n"
        md += "|:----:|:--------:|\n"
        
        for i, char in enumerate(self.characters, 1):
            if char == ' ':
                md += f"| {i} | ` ` (espacio) |\n"
            else:
                md += f"| {i} | `{char}` |\n"
        
        md += f"| {len(self.characters) + 1} | fin de línea |\n\n"
        
        md += "**Lexemas identificados:**\n"
        md += f"{' '.join(self.lexemes)}\n\n"
        
        md += " En esta etapa **no se evalúa nada**, solo se **segmenta** el flujo de caracteres en **palabras válidas (lexemas)**.\n\n"
        md += "---\n"
        
        return md