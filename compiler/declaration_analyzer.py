# compiler/declaration_analyzer.py

import re
from .symbol_tables import VariableSymbolTable

class DeclarationAnalyzer:
    """
    Analiza la sección de declaraciones de variables (bloque VAR) 
    y construye la tabla de símbolos variables.
    """
    
    def __init__(self, symbol_table=None):
        self.symbol_table = symbol_table if symbol_table is not None else VariableSymbolTable()
    
    def analyze_declarations(self, code_string):
        """
        Analiza el código y extrae las declaraciones de variables del bloque VAR.
        Retorna la tabla de símbolos variables actualizada.
        """
        # Limpiar el código: eliminar comentarios y normalizar espacios
        clean_code = self._clean_code(code_string)
        
        # Buscar el bloque VAR
        var_pattern = r'\bvar\b(.*?)(?:\bbegin\b|\bend\b|\bprocedure\b|\bfunction\b|$)'
        var_match = re.search(var_pattern, clean_code, re.IGNORECASE | re.DOTALL)
        
        if not var_match:
            return self.symbol_table  # No hay declaraciones
        
        var_section = var_match.group(1)
        
        # Dividir por líneas y procesar cada declaración
        lines = var_section.split(';')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Buscar patrones: "variable : tipo" o "variable1, variable2 : tipo"
            if ':' in line:
                # Separar la parte de variables y el tipo
                vars_part, type_part = line.split(':', 1)
                var_type = type_part.strip().lower()
                
                # Separar variables por comas
                variables = [v.strip() for v in vars_part.split(',')]
                
                for var_name in variables:
                    if var_name:  # Asegurarse que no esté vacío
                        self.symbol_table.add_symbol(var_name, var_type)
        
        return self.symbol_table
    
    def _clean_code(self, code_string):
        """Limpia el código removiendo comentarios y espacios extras."""
        # Remover comentarios de una línea { ... }
        code_string = re.sub(r'\{[^}]*\}', '', code_string)
        # Remover comentarios de una línea (* ... *)
        code_string = re.sub(r'\(\*[^*]*\*\)', '', code_string)
        # Normalizar espacios
        code_string = re.sub(r'\s+', ' ', code_string)
        return code_string
    
    def get_undeclared_variables(self, tokens):
        """
        Verifica si hay variables usadas pero no declaradas.
        Retorna lista de variables no declaradas.
        """
        declared_vars = {info['name'] for info in self.symbol_table.symbols.values()}
        used_vars = set()
        
        for token_type, value, table_id in tokens:
            # Solo considerar IDENTIFIER que están marcados como UNDECLARED
            # Ignorar PROGRAM_NAME y otros tipos de tokens
            if token_type == 'IDENTIFIER' and table_id == 'UNDECLARED':
                used_vars.add(value.lower())
        
        return used_vars