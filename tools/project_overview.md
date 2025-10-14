# Estructura del proyecto

```
ProcesoCompilacion
├── compiler
│   ├── __init__.py
│   ├── intermediate_code_gen.py
│   ├── lexical_analyzer.py
│   ├── pipeline.py
│   ├── semantic_analyzer.py
│   ├── structures.py
│   ├── symbol_tables.py
│   ├── syntactic_checking.py
│   └── syntax_analizer.py
├── reports
│   ├── reporte_compilacion.md
│   ├── reporte_flag.md
│   ├── reporte_message.md
│   ├── reporte_mixed.md
│   ├── reporte_result.md
│   └── reporte_x.md
├── README.md
└── main.py
```

## `main.py`

```python
# main.py

from compiler.pipeline import CompilationPipeline
from compiler.symbol_tables import VariableSymbolTable

if __name__ == "__main__":
    # Ejemplo con diferentes tipos
    expressions = [
        # "x := 1 + a + (b * c) + 3",  # Enteros
        # "result := 3.14 * radius + 2.5",  # Reales
        # "message := 'Hola ' + 'Mundo'",  # Strings
        # "flag := (x > 5) and (y < 10)",  # Booleanos
        # "mixed := 10 + 3.14"  # Mixed types
    ]
    
    for expression in expressions:
        print(f"\n{'='*50}")
        print(f"Compilando: {expression}")
        print(f"{'='*50}")
        
        symbol_table = VariableSymbolTable()
        
        # Definir símbolos según la expresión
        if "message :=" in expression:
            symbol_table.add_symbol('message', 'string')
        elif "result :=" in expression:
            symbol_table.add_symbol('result', 'real')
            symbol_table.add_symbol('radius', 'real')
        elif "flag :=" in expression:
            symbol_table.add_symbol('flag', 'boolean')
            symbol_table.add_symbol('x', 'integer')
            symbol_table.add_symbol('y', 'integer')
        elif "mixed :=" in expression:
            symbol_table.add_symbol('mixed', 'real')
        else:
            # Default: enteros
            symbol_table.add_symbol('x', 'integer')
            symbol_table.add_symbol('a', 'integer')
            symbol_table.add_symbol('b', 'integer') 
            symbol_table.add_symbol('c', 'integer')
        
        pipeline = CompilationPipeline(expression, symbol_table)
        
        try:
            pipeline.run()
            pipeline.save_report(f"reports/reporte_{expression.split()[0]}.md")
            print(f" Compilación exitosa para: {expression}")
        except ValueError as e:
            print(f" ERROR: {e}")```

## `compiler\__init__.py`

```python
```

## `compiler\intermediate_code_gen.py`

```python
# compiler/intermediate_code_gen.py

from .syntax_analizer import Node # Importamos la clase Node del analizador sintáctico

class IntermediateCodeGenerator:
    """
    Genera código intermedio (postfijo y tripletas) a partir de un
    Árbol de Sintaxis Abstracta (AST).
    """
    def __init__(self, ast_root: Node):
        self.ast_root = ast_root
        self.triples = []
        self.temp_counter = 0 # Para futuras cuádruplas

    def generate(self):
        """Genera el reporte de código intermedio."""
        # Generamos las tripletas caminando por el árbol.
        self._walk_ast(self.ast_root)
        
        # Generamos la notación postfija a partir del AST para evitar redundancia.
        postfix = self._generate_postfix_from_ast(self.ast_root)
        
        return self._generate_markdown(postfix, self.triples)

    def _walk_ast(self, node: Node):
        """
        Recorre el AST de forma recursiva (post-orden) para generar las tripletas.
        Devuelve el 'nombre' del resultado (una variable, un número o una referencia a una tripleta).
        """
        # Caso base: si el nodo es una hoja (operando), devolvemos su valor.
        if not node.left and not node.right:
            return node.value

        # Paso recursivo: procesar los hijos primero.
        left_result = self._walk_ast(node.left)
        right_result = self._walk_ast(node.right)
        
        # Emitir la tripleta para el nodo actual.
        op = node.value
        index = len(self.triples)
        self.triples.append([op, left_result, right_result])
        
        # El "resultado" de esta operación es una referencia a la tripleta que acabamos de crear.
        return f'({index})'

    def _generate_postfix_from_ast(self, node: Node):
        """Genera la notación postfija recorriendo el AST en post-orden."""
        if not node:
            return []
        
        left = self._generate_postfix_from_ast(node.left)
        right = self._generate_postfix_from_ast(node.right)
        
        return left + right + [node.value]

    def _generate_markdown(self, postfix_list, triples_list):
        md = "## 3. Representación Intermedia\n\n"
        md += "### Notación Postfija (Polaca Inversa)\n"
        md += f"`{' '.join(postfix_list)}`\n\n"
        md += "### Tripletas\n"
        md += "La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:\n\n"
        md += "| # | Operador | Operando 1 | Operando 2 |\n"
        md += "|---|----------|------------|------------|\n"
        for i, (op, arg1, arg2) in enumerate(triples_list):
            md += f"|({i})| `{op}`     | `{arg1}`     | `{arg2}`     |\n"
        return md```

## `compiler\lexical_analyzer.py`

```python
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
        return md```

## `compiler\pipeline.py`

```python
# compiler/pipeline.py

from .lexical_analyzer import LexicalAnalyzer
from .syntax_analizer import SyntaxAnalyzer
from .syntactic_checking import SyntacticChecking
from .semantic_analyzer import SemanticAnalyzer
from .intermediate_code_gen import IntermediateCodeGenerator
from .symbol_tables import generate_fixed_tables_report

class CompilationPipeline:
    def __init__(self, expression, symbol_table=None):
        self.expression = expression
        self.symbol_table = symbol_table
        self.report = f"# Reporte de Compilación para la Expresión\n\n`{expression}`\n\n---\n"

    def run(self):
        self.report += "\n# Fase 1: Análisis\n"

        print("Iniciando Fase 1.1: Análisis Lexicográfico...")
        # MODIFICACIÓN: Pasar la tabla de símbolos al LexicalAnalyzer si existe
        lex_analyzer = LexicalAnalyzer(self.expression, self.symbol_table)
        tokens, lex_report = lex_analyzer.analyze()
        self.report += lex_report + "\n---\n"

        # AGREGAR reportes de tablas
        self.report += generate_fixed_tables_report() + "\n"
        self.report += lex_analyzer.symbol_table.generate_markdown_report() + "\n---\n"

        self.report += "\n## Fase 1.2: Análisis Sintáctico\n"

        print("Iniciando Fase 1.2.1: Generación de Árbol de Expresión...")
        syntax_tokens = [(kind, value) for kind, value, _ in tokens]
        syntax_analyzer = SyntaxAnalyzer(syntax_tokens)
        ast_root, syntax_report = syntax_analyzer.analyze()
        self.report += syntax_report + "\n---\n"

        print("Iniciando Fase 1.2.2: Comprobación Sintáctica (Árbol de Derivación)...")
        sc_analizer = SyntacticChecking(syntax_tokens)
        parse_tree, sc_report = sc_analizer.analyze()
        self.report += sc_report + "\n---\n"

        print("Iniciando Fase 1.3: Análisis Semántico...")
        semantic_analyzer = SemanticAnalyzer(ast_root, lex_analyzer.symbol_table)
        annotated_ast, semantic_report = semantic_analyzer.analyze()
        self.report += semantic_report + "\n---\n"

        self.report += "\n# Fase 2: Síntesis\n"

        print("Iniciando Fase 2.1: Generación de Código Intermedio...")
        icg = IntermediateCodeGenerator(annotated_ast)
        icg_report = icg.generate()
        self.report += icg_report

    def save_report(self, filename="reports/reporte_compilacion.md"):
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.report)
        print(f"\n ¡Reporte guardado exitosamente en '{filename}'!")```

## `compiler\semantic_analyzer.py`

```python
# compiler/semantic_analyzer.py

from .syntax_analizer import Node
from .symbol_tables import VariableSymbolTable, TypeSystem

class SemanticAnalyzer:
    def __init__(self, ast_root: Node, symbol_table: VariableSymbolTable):
        self.ast_root = ast_root
        self.symbol_table = symbol_table
        self.errors = []

    def analyze(self):
        """
        Ejecuta el análisis de tipos y devuelve el AST anotado y un reporte.
        """
        self.errors = []
        self._annotate_tree(self.ast_root)
        report = self._generate_markdown()
        return self.ast_root, report

    def _annotate_tree(self, node: Node):
        """
        Recorre el árbol (post-orden) para asignar y verificar tipos.
        """
        if not node:
            return

        # Si es una hoja (operando)
        if not node.left and not node.right:
            # Detección de tipos (código existente)
            if node.value.isdigit():
                node.type = 'integer'
                node.addressing_mode = 'immediate'
            elif (node.value.replace('.', '').replace('-', '').isdigit() and 
                  node.value.count('.') == 1 and
                  (node.value[0] == '-' or node.value[0].isdigit())):
                node.type = 'real'
                node.addressing_mode = 'immediate'
            elif node.value in ['true', 'false']:
                node.type = 'boolean'
                node.addressing_mode = 'immediate'
            elif node.value.startswith("'") and node.value.endswith("'"):
                node.type = 'char'
                node.addressing_mode = 'immediate'
            elif node.value.startswith('"') and node.value.endswith('"'):
                node.type = 'string'
                node.addressing_mode = 'immediate'
            else:
                # Buscar en tabla de símbolos variables
                symbol = self.symbol_table.find_symbol_by_name(node.value)
                if symbol:
                    node.type = symbol.type
                    node.addressing_mode = symbol.mode
                    node.memory_address = symbol.address
                else:
                    node.type = f'ERROR: Variable \'{node.value}\' no declarada'
                    node.addressing_mode = 'error'
                    self.errors.append(node.type)
            return

        # Recorrer recursivamente los hijos primero
        self._annotate_tree(node.left)
        if node.right:  # Solo si existe hijo derecho (operadores binarios)
            self._annotate_tree(node.right)

        # --- Verificación de tipos usando el sistema de tipos ---
        op = node.value
        
        # Manejar operador unario 'not'
        if op == 'not':
            if not node.left:
                node.type = 'ERROR: Operador unario "not" requiere un operando'
                self.errors.append(node.type)
                return
                
            operand_type = node.left.type
            if operand_type == 'boolean':
                node.type = 'boolean'
            else:
                node.type = f'ERROR: Operador "not" no puede aplicarse a {operand_type}'
                self.errors.append(node.type)
            
            node.addressing_mode = 'register'
            return

        # Para operadores binarios
        left_type = node.left.type if node.left else None
        right_type = node.right.type if node.right else None

        # Usar el sistema de tipos para determinar el tipo resultante
        result_type = TypeSystem.get_result_type(op, left_type, right_type)
        
        if result_type:
            node.type = result_type
        else:
            node.type = f'ERROR: Operación \'{op}\' no permitida entre {left_type} y {right_type}'
            self.errors.append(node.type)

        # --- Determinación de modo de direccionamiento ---
        if node.value in ['+', '-', '*', '/', '=', '<>', '<', '>', '<=', '>=', 'and', 'or']:
            node.addressing_mode = 'register'
        elif node.value == ':=':
            # Verificar compatibilidad de asignación
            if not TypeSystem.can_convert(right_type, left_type) and not 'ERROR' in left_type and not 'ERROR' in right_type:
                node.type = f'ERROR: No se puede asignar {right_type} a {left_type}'
                self.errors.append(node.type)
            node.addressing_mode = 'direct'
        elif not hasattr(node, 'addressing_mode'):
            node.addressing_mode = 'direct'

    # ... (el resto del código se mantiene igual)
    def _generate_markdown(self):
        """Genera el reporte Markdown con el árbol semántico anotado."""
        md = "## 1.3. Análisis Semántico\n\n"
        
        if self.errors:
            md += "### Errores Semánticos Encontrados\n\n"
            for error in set(self.errors):  # Mostrar errores únicos
                md += f"- {error}\n"
            md += "\n"
        
        md += "Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.\n\n"
        md += "```mermaid\n"
        md += "graph TD\n"
        md += "    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;\n"
        md += "    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;\n"
        md += "    classDef immediate fill:#ddddff,stroke:#44d,stroke-width:2px;\n"
        
        def traverse(node):
            lines = []
            node_type = node.type if node.type else "indefinido"
            
            # Determinar clase CSS basada en tipo y modo
            if "ERROR" in node_type:
                style_class = "error"
            elif getattr(node, 'addressing_mode', '') == 'immediate':
                style_class = "immediate"
            else:
                style_class = "default"
                
            addressing_info = f"<br/>Modo: {getattr(node, 'addressing_mode', 'N/A')}"
            if hasattr(node, 'memory_address'):
                addressing_info += f"<br/>Addr: {node.memory_address}"
                
            label = f'["<b>{node.value}</b><br/><i>{node_type}</i>{addressing_info}"]'
            lines.append(f"    {node.id}{label}:::{style_class}")

            if node.left:
                lines.extend(traverse(node.left))
                lines.append(f"    {node.id} --> {node.left.id}")
            if node.right:
                lines.extend(traverse(node.right))
                lines.append(f"    {node.id} --> {node.right.id}")
            return lines

        mermaid_lines = traverse(self.ast_root)
        md += "\n".join(mermaid_lines)
        md += "\n```\n"
        
        # Agregar resumen de tipos
        md += "\n### Resumen de Tipos en la Expresión\n\n"
        type_count = {}
        def count_types(node):
            if hasattr(node, 'type') and node.type:
                if "ERROR" not in node.type:
                    type_count[node.type] = type_count.get(node.type, 0) + 1
            if node.left:
                count_types(node.left)
            if node.right:
                count_types(node.right)
        
        count_types(self.ast_root)
        for type_name, count in type_count.items():
            md += f"- **{type_name}**: {count} ocurrencias\n"
        
        return md```

## `compiler\structures.py`

```python
# compiler/structures.py

import itertools

class Node:
    """Estructura de datos para un nodo del árbol sintáctico."""
    # Usamos un generador global simple para los IDs
    id_counter = itertools.count()

    def __init__(self, symbol):
        self.id = f"n{next(self.id_counter)}"
        self.symbol = symbol
        self.children = []

    def add_child(self, child):
        if child:
            self.children.append(child)```

## `compiler\symbol_tables.py`

```python
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
        
    return md```

## `compiler\syntactic_checking.py`

```python
# compiler/syntactic_checking.py

from .structures import Node

class SyntacticChecking:
    """Construye el árbol de derivación y genera un reporte."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def analyze(self):
        """Realiza el análisis y devuelve el árbol y el reporte."""
        try:
            parse_tree = self._parse()
            report = self._generate_markdown(parse_tree)
            return parse_tree, report
        except Exception as e:
            # Si hay error, generar un reporte de error
            error_report = f"### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos\n\n"
            error_report += f"**Error de sintaxis:** {str(e)}\n\n"
            error_report += "La secuencia de tokens no pudo ser validada completamente por la gramática.\n"
            return None, error_report

    def _current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def _consume(self, expected_type=None):
        kind, val = self._current_token()
        if expected_type and kind != expected_type:
            raise ValueError(f"Error de sintaxis: Se esperaba {expected_type} pero se encontró {kind} ('{val}')")
        self.pos += 1
        return kind, val

    def _parse(self):
        # La gramática sigue siendo S -> ID := E
        root = Node("S")
        
        id_val = self._consume('IDENTIFIER')[1]
        id_node = Node("ID")
        id_node.add_child(Node(id_val))
        root.add_child(id_node)

        assign_kind, assign_val = self._consume()
        if assign_kind != 'OPERATOR' or assign_val != ':=':
            raise ValueError(f"Error de sintaxis: Se esperaba operador ':=' pero se encontró {assign_kind} ('{assign_val}')")
        root.add_child(Node(assign_val))
        
        root.add_child(self._e())

        # Verificar que no queden tokens por consumir
        if self._current_token()[0] != 'EOF':
            raise ValueError(f"Error de sintaxis: Tokens extra al final de la expresión: {self._current_token()}")
        return root
    
    def _e(self):
        node_e = self._t()
        # Operadores lógicos binarios
        while (self._current_token()[0] == 'OPERATOR' and 
               self._current_token()[1] in ('and', 'or')):
            op_val = self._consume('OPERATOR')[1]
            parent_e = Node("E")
            parent_e.add_child(node_e)
            parent_e.add_child(Node(op_val))
            parent_e.add_child(self._t())
            node_e = parent_e
        return node_e

    def _t(self):
        node_t = self._f()
        # Operadores de comparación
        while (self._current_token()[0] == 'OPERATOR' and 
               self._current_token()[1] in ('=', '<', '>', '<=', '>=', '<>')):
            op_val = self._consume('OPERATOR')[1]
            parent_t = Node("T")
            parent_t.add_child(node_t)
            parent_t.add_child(Node(op_val))
            parent_t.add_child(self._f())
            node_t = parent_t
        return node_t

    def _f(self):
        node_f = self._g()
        # Operadores + y -
        while (self._current_token()[0] == 'OPERATOR' and 
               self._current_token()[1] in ('+', '-')):
            op_val = self._consume('OPERATOR')[1]
            parent_f = Node("F")
            parent_f.add_child(node_f)
            parent_f.add_child(Node(op_val))
            parent_f.add_child(self._g())
            node_f = parent_f
        return node_f

    def _g(self):
        node_g = self._h()
        # Operadores * y /
        while (self._current_token()[0] == 'OPERATOR' and 
               self._current_token()[1] in ('*', '/')):
            op_val = self._consume('OPERATOR')[1]
            parent_g = Node("G")
            parent_g.add_child(node_g)
            parent_g.add_child(Node(op_val))
            parent_g.add_child(self._h())
            node_g = parent_g
        return node_g

    def _h(self):
        # Manejar operador unario 'not'
        if (self._current_token()[0] == 'OPERATOR' and 
            self._current_token()[1] == 'not'):
            op_val = self._consume('OPERATOR')[1]
            node_h = Node("H")
            node_h.add_child(Node(op_val))
            node_h.add_child(self._h())  # Aplicar 'not' a la siguiente expresión
            return node_h
        
        return self._i()

    def _i(self):
        kind, val = self._current_token()
        node_i = Node("I")
        if val == '(':
            self._consume()  # Consumir '('
            node_i.add_child(self._e())  # IMPORTANTE: llamar a _e() no a _i()
            if self._current_token()[1] != ')':
                raise ValueError(f"Error de sintaxis: Se esperaba ')' pero se encontró {self._current_token()}")
            self._consume()  # Consumir ')'
        elif kind == 'IDENTIFIER':
            self._consume('IDENTIFIER')
            id_node = Node("ID")
            id_node.add_child(Node(val))
            node_i.add_child(id_node)
        elif kind == 'CONSTANT':
            self._consume('CONSTANT')
            num_node = Node("NUM")
            num_node.add_child(Node(val))
            node_i.add_child(num_node)
        elif kind == 'STRING':
            self._consume('STRING')
            str_node = Node("STRING")
            str_node.add_child(Node(val))
            node_i.add_child(str_node)
        else:
            raise ValueError(f"Sintaxis inválida, se esperaba IDENTIFIER, CONSTANT, STRING o '(', se encontró {kind} ('{val}')")
        return node_i

    def _generate_markdown(self, root_node):
        md = "### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos\n\n"
        md += "La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:\n\n"
        md += "```mermaid\n"
        md += "graph TD\n"
        
        connections = []
        q = [root_node]
        visited = {root_node.id}
        while q:
            node = q.pop(0)
            for child in node.children:
                if child.id not in visited:
                    connections.append(f"    {node.id}['{node.symbol}'] --- {child.id}['{child.symbol}']")
                    visited.add(child.id)
                    q.append(child)
        md += "\n".join(connections)
        md += "\n```\n"
        return md```

## `compiler\syntax_analizer.py`

```python
# compiler/syntax_analizer.py

import re

# --- Definiciones de Operadores ---
precedence = {
    ':=': 0,
    'and': 1, 'or': 1,                          # Operadores lógicos binarios
    'not': 2,                                   # Operador lógico unario (alta precedencia)
    '=': 3, '<': 3, '>': 3, '<=': 3, '>=': 3, '<>': 3,  # Operadores de comparación
    '+': 4, '-': 4,
    '*': 5, '/': 5
}

associativity = {
    ':=': 'right',
    'and': 'left', 'or': 'left',
    'not': 'right',  # 'not' es asociativo por la derecha
    '=': 'left', '<': 'left', '>': 'left', '<=': 'left', '>=': 'left', '<>': 'left',
    '+': 'left', '-': 'left',
    '*': 'left', '/': 'left'
}

# --- Estructura de Datos para el AST ---
class Node:
    """Nodo para un Árbol de Sintaxis Abstracta (AST)."""
    # Usamos un contador simple para los IDs de Mermaid
    _counter = 0
    
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.id = f"N{Node._counter}"
        Node._counter += 1

class SyntaxAnalyzer:
    """
    Genera un Árbol de Sintaxis Abstracta (AST) usando Shunting-yard.
    """
    def __init__(self, tokens):
        # Tokens recibidos del analizador léxico
        self.tokens = tokens
        Node._counter = 0 # Reiniciar contador de nodos para cada análisis

    def analyze(self):
        """Realiza el análisis y devuelve el árbol y el reporte."""
        postfix_tokens = self._infix_to_postfix()
        ast_root = self._build_tree(postfix_tokens)
        report = self._generate_markdown(ast_root, postfix_tokens)
        return ast_root, report

    def _infix_to_postfix(self):
        """Convierte la lista de tokens infijos a postfijos."""
        output = []
        stack = []
        
        for kind, value in self.tokens:
            # ACTUALIZADO: Incluir 'STRING' como operando
            if kind in ['IDENTIFIER', 'CONSTANT', 'STRING']:
                output.append(value)
            elif value in precedence:  # Es un operador
                # Manejar operadores unarios (como 'not')
                if value == 'not':
                    stack.append(value)
                else:
                    while (stack and stack[-1] in precedence and
                           ((associativity[value] == 'left' and precedence[stack[-1]] >= precedence[value]) or
                            (associativity[value] == 'right' and precedence[stack[-1]] > precedence[value]))):
                        output.append(stack.pop())
                    stack.append(value)
            elif value == '(':
                stack.append(value)
            elif value == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack and stack[-1] == '(':
                    stack.pop()  # Quitar '(' de la pila
                else:
                    raise ValueError("Paréntesis de cierre sin apertura correspondiente")
        
        while stack:
            token = stack.pop()
            if token == '(':
                raise ValueError("Paréntesis de apertura sin cierre correspondiente")
            output.append(token)
            
        return output

    def _build_tree(self, postfix_tokens):
        """Construye el AST a partir de una lista de tokens postfijos."""
        stack = []
        operators = precedence.keys()
        
        for token in postfix_tokens:
            if token in operators:
                if token == 'not':  # Operador unario
                    if len(stack) < 1:
                        raise ValueError(f"Error de sintaxis: Operador unario '{token}' sin operando. Stack: {stack}")
                    operand = stack.pop()
                    stack.append(Node(token, operand, None))  # Solo hijo izquierdo
                else:  # Operador binario
                    if len(stack) < 2:
                        raise ValueError(f"Error de sintaxis: Operador '{token}' sin suficientes operandos. Stack: {stack}")
                    right = stack.pop()
                    left = stack.pop()
                    stack.append(Node(token, left, right))
            else:  # Es un operando
                stack.append(Node(token))
        
        if len(stack) != 1:
            raise ValueError(f"Error de sintaxis: Expresión inválida. Stack final: {stack}")
        return stack[0]

    def _generate_markdown(self, root, postfix_tokens):
        """Genera el reporte Markdown con el diagrama Mermaid del AST."""
        md = "### 1.2.1. Generación de Árbol de Expresión\n\n"
        md += "La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.\n\n"
        md += f"**Notación Postfija intermedia:** `{' '.join(postfix_tokens)}`\n\n"
        md += "```mermaid\n"
        md += "graph TD\n"
        
        # Función interna para recorrer el árbol y generar las líneas de Mermaid
        def traverse(node):
            lines = []
            # Estilo para el nodo actual
            if node.value in precedence:
                lines.append(f"    {node.id}(('{node.value}'))")  # Círculo para operadores
            else:
                lines.append(f"    {node.id}(['{node.value}'])")  # Rectángulo para operandos
            
            # Conexiones con los hijos
            if node.left:
                lines.extend(traverse(node.left))
                lines.append(f"    {node.id} --> {node.left.id}")
            if node.right:
                lines.extend(traverse(node.right))
                lines.append(f"    {node.id} --> {node.right.id}")
            return lines

        mermaid_lines = traverse(root)
        md += "\n".join(mermaid_lines)
        md += "\n```\n"
        return md```

