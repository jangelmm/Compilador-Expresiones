# compiler/symbol_tables.py

# Tablas Fijas
RESERVED_WORDS = {
    'var': 1, 'proc': 2, 'begin': 3, 'end': 4, 
    'integer': 5, 'char': 6, 'real': 7
}

OPERATORS = {
    ':=': 101, '+': 102, '-': 103, '*': 104, '/': 105,
    # Operadores de comparación y lógicos
    '=': 106, '<': 107, '>': 108, '<=': 109, '>=': 110, '<>': 111,
    'and': 112, 'or': 113, 'not': 114  # AGREGADO: 'not'
}

DELIMITERS = {
    ':': 201, ';': 202, '(': 203, ')': 204
}


class VariableSymbolTable:
    def __init__(self):
        self.symbols = {}
        self.address_counter = 0x1000  # Dirección base en RAM
        self.scope_stack = [0]  # Scope global inicial
        
    def add_symbol(self, name, symbol_type, value=None, scope=None):
        if scope is None:
            scope = self.scope_stack[-1]
        symbol_id = self._generate_hash(name, scope)
        self.symbols[symbol_id] = {
            'name': name,
            'type': symbol_type,
            'value': value,
            'scope': scope,
            'address': f"{self.address_counter:04X}",
            'mode': 'direct'  # Modo de direccionamiento
        }
        self.address_counter += 4  # Incremento para siguiente símbolo
        return symbol_id
    
    def _generate_hash(self, name, scope):
        # Función hash simple para generar IDs únicos considerando el scope
        return hash(f"{name}_{scope}") % 1000 + 10000

    def generate_markdown_report(self):
        md = "## Tabla de Símbolos Variables\n\n"
        md += "| ID | Nombre | Tipo | Scope | Dirección | Modo |\n"
        md += "|----|--------|------|-------|-----------|------|\n"
        
        for symbol_id, info in self.symbols.items():
            md += f"| {symbol_id} | {info['name']} | {info['type']} | "
            md += f"{info['scope']} | {info['address']} | {info['mode']} |\n"
        
        # Agregar resumen
        md += f"\n**Total de símbolos:** {len(self.symbols)}\n"
        md += f"**Siguiente dirección disponible:** {self.address_counter:04X}\n"
        
        return md
    
    def find_symbol_by_name(self, name):
        """
        Busca un símbolo por nombre en la tabla.
        Retorna la información del símbolo o None si no existe.
        """
        for symbol_id, symbol_info in self.symbols.items():
            if symbol_info['name'] == name:
                # Crear un objeto simple con los atributos necesarios
                class Symbol:
                    pass
                symbol = Symbol()
                symbol.type = symbol_info['type']
                symbol.mode = symbol_info['mode']
                symbol.address = symbol_info['address']
                return symbol
        return None

class TypeSystem:
    """
    Sistema de tipos para verificar compatibilidad y determinar tipos resultantes.
    """
    
    # Tabla de compatibilidad de tipos para operaciones
    TYPE_COMPATIBILITY = {
        # Operaciones aritméticas
        '+': {
            ('integer', 'integer'): 'integer',
            ('real', 'real'): 'real',
            ('integer', 'real'): 'real',
            ('real', 'integer'): 'real',
            ('string', 'string'): 'string',
        },
        '-': {
            ('integer', 'integer'): 'integer',
            ('real', 'real'): 'real',
            ('integer', 'real'): 'real',
            ('real', 'integer'): 'real',
        },
        '*': {
            ('integer', 'integer'): 'integer',
            ('real', 'real'): 'real',
            ('integer', 'real'): 'real',
            ('real', 'integer'): 'real',
        },
        '/': {
            ('integer', 'integer'): 'real',
            ('real', 'real'): 'real',
            ('integer', 'real'): 'real',
            ('real', 'integer'): 'real',
        },
        # Operaciones de comparación
        '=': {
            ('integer', 'integer'): 'boolean',
            ('real', 'real'): 'boolean',
            ('integer', 'real'): 'boolean',
            ('real', 'integer'): 'boolean',
            ('boolean', 'boolean'): 'boolean',
            ('string', 'string'): 'boolean',
            ('char', 'char'): 'boolean',
        },
        '<>': {
            ('integer', 'integer'): 'boolean',
            ('real', 'real'): 'boolean',
            ('integer', 'real'): 'boolean',
            ('real', 'integer'): 'boolean',
            ('boolean', 'boolean'): 'boolean',
            ('string', 'string'): 'boolean',
            ('char', 'char'): 'boolean',
        },
        '<': {
            ('integer', 'integer'): 'boolean',
            ('real', 'real'): 'boolean',
            ('integer', 'real'): 'boolean',
            ('real', 'integer'): 'boolean',
        },
        '>': {
            ('integer', 'integer'): 'boolean',
            ('real', 'real'): 'boolean',
            ('integer', 'real'): 'boolean',
            ('real', 'integer'): 'boolean',
        },
        '<=': {
            ('integer', 'integer'): 'boolean',
            ('real', 'real'): 'boolean',
            ('integer', 'real'): 'boolean',
            ('real', 'integer'): 'boolean',
        },
        '>=': {
            ('integer', 'integer'): 'boolean',
            ('real', 'real'): 'boolean',
            ('integer', 'real'): 'boolean',
            ('real', 'integer'): 'boolean',
        },
        # Operaciones lógicas
        'and': {
            ('boolean', 'boolean'): 'boolean',
        },
        'or': {
            ('boolean', 'boolean'): 'boolean',
        },
        'not': {
            ('boolean',): 'boolean',  # 'not' aplicado a boolean devuelve boolean
        }
    }
    
    # Tabla de conversiones permitidas
    CONVERSIONS = {
        'integer': ['real'],  # integer se puede convertir a real
        'real': [],           # real no se puede convertir a integer automáticamente
        'boolean': [],
        'string': [],
        'char': ['string']    # char se puede convertir a string
    }

    @staticmethod
    def get_result_type(operator, left_type, right_type):
        """
        Determina el tipo resultante de una operación entre dos tipos.
        Retorna None si la operación no es válida.
        """
        # Limpiar tipos que tengan "ERROR" en el nombre
        if 'ERROR' in str(left_type) or (right_type and 'ERROR' in str(right_type)):
            return None
            
        # Para asignación, el tipo resultante es el tipo del lado izquierdo
        if operator == ':=':
            return left_type
            
        # Para operador unario 'not'
        if operator == 'not':
            if left_type == 'boolean':
                return 'boolean'
            return None
            
        # Buscar en la tabla de compatibilidad
        if operator in TypeSystem.TYPE_COMPATIBILITY:
            compatibility_table = TypeSystem.TYPE_COMPATIBILITY[operator]
            
            # Buscar combinación exacta
            if (left_type, right_type) in compatibility_table:
                return compatibility_table[(left_type, right_type)]
            
            # Si no encuentra combinación exacta, retornar None (error)
            return None
        
        return None

    @staticmethod
    def can_convert(from_type, to_type):
        """
        Verifica si un tipo puede convertirse automáticamente a otro.
        """
        if from_type == to_type:
            return True
            
        if from_type in TypeSystem.CONVERSIONS:
            return to_type in TypeSystem.CONVERSIONS[from_type]
            
        return False

def generate_fixed_tables_report():
    md = "## Tablas Fijas del Lenguaje\n\n"
    
    md += "### Palabras Reservadas\n"
    md += "| ID | Palabra |\n|----|---------|\n"
    for word, id_val in RESERVED_WORDS.items():
        md += f"| {id_val} | {word} |\n"
    
    md += "\n### Operadores\n"
    md += "| ID | Operador |\n|----|----------|\n"
    for op, id_val in OPERATORS.items():
        md += f"| {id_val} | {op} |\n"
    
    md += "\n### Delimitadores\n"
    md += "| ID | Delimitador |\n|----|-------------|\n"
    for delim, id_val in DELIMITERS.items():
        md += f"| {id_val} | {delim} |\n"
        
    return md