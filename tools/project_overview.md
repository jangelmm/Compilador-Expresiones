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
│   ├── syntactic_checking.py
│   └── syntax_analizer.py
├── reports
│   └── reporte_compilacion.md
├── README.md
└── main.py
```

## `main.py`

```python
# main.py

from compiler.pipeline import CompilationPipeline

if __name__ == "__main__":
    expression_a_evaluar = "x := 1 + a + (b * c) + 3"

    # Define una tabla de símbolos de ejemplo para la prueba
    tabla_de_simbolos_ejemplo = {
        'x': 'int',
        'a': 'int',
        'b': 'int',
        'c': 'int'
    }
    
    # --- CAMBIO CLAVE AQUÍ ---
    # Pasamos la tabla de símbolos al crear el pipeline
    pipeline = CompilationPipeline(expression_a_evaluar, tabla_de_simbolos_ejemplo)
    
    try:
        pipeline.run()
        pipeline.save_report()
    except ValueError as e:
        print(f"\n ERROR DURANTE LA COMPILACIÓN: {e}")```

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
        return md```

## `compiler\pipeline.py`

```python
# compiler/pipeline.py

from .lexical_analyzer import LexicalAnalyzer
from .syntax_analizer import SyntaxAnalyzer
from .syntactic_checking import SyntacticChecking
from .semantic_analyzer import SemanticAnalyzer  # Asegúrate de que este archivo y clase existan
from .intermediate_code_gen import IntermediateCodeGenerator

class CompilationPipeline:
    """Clase principal que gestiona todo el proceso de compilación."""

    # --- CAMBIO CLAVE AQUÍ ---
    def __init__(self, expression, symbol_table): # 1. Aceptar symbol_table como argumento
        self.expression = expression
        self.symbol_table = symbol_table       # 2. Guardarla en el objeto self
        self.report = f"# Reporte de Compilación para la Expresión\n\n`{expression}`\n\n---\n"

    def run(self):
        self.report += "\n# Fase 1: Análisis\n"

        print("Iniciando Fase 1.1: Análisis Lexicográfico...")
        lex_analyzer = LexicalAnalyzer(self.expression)
        tokens, lex_report = lex_analyzer.analyze()
        self.report += lex_report + "\n---\n"

        self.report += "\n## Fase 1.2: Análisis Sintáctico\n"

        print("Iniciando Fase 1.2.1: Generación de Árbol de Expresión...")
        syntax_analyzer = SyntaxAnalyzer(list(tokens))
        ast_root, syntax_report = syntax_analyzer.analyze() # Capturamos el AST
        self.report += syntax_report + "\n---\n"

        print("Iniciando Fase 1.2.2: Comprobación Sintáctica (Árbol de Derivación)...")
        sc_analizer = SyntacticChecking(list(tokens))
        _, sc_report = sc_analizer.analyze()
        self.report += sc_report + "\n---\n"

        print("Iniciando Fase 1.3: Análisis Semántico...")
        # Ahora self.symbol_table existe y la llamada es correcta
        semantic_analyzer = SemanticAnalyzer(ast_root, self.symbol_table)
        annotated_ast, semantic_report = semantic_analyzer.analyze()
        self.report += semantic_report + "\n---\n"

        self.report += "\n# Fase 2: Síntesis\n"

        print("Iniciando Fase 2.1: Generación de Código Intermedio...")
        # El generador de código intermedio debería usar el AST anotado
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

from .syntax_analizer import Node # Importamos la clase Node del AST

class SemanticAnalyzer:
    """
    Realiza el análisis semántico recorriendo el AST para verificar tipos.
    """
    def __init__(self, ast_root: Node, symbol_table: dict):
        """
        Inicializa el analizador con el AST y una tabla de símbolos.
        """
        self.ast_root = ast_root
        self.symbol_table = symbol_table

    def analyze(self):
        """
        Ejecuta el análisis de tipos y devuelve el AST anotado y un reporte.
        """
        # La función de anotación modifica el AST directamente
        self._annotate_tree(self.ast_root)
        report = self._generate_markdown()
        return self.ast_root, report

    def _annotate_tree(self, node: Node):
        """
        Recorre el árbol (post-orden) para asignar y verificar tipos.
        Esta función MODIFICA el árbol, añadiendo el atributo .type a cada nodo.
        """
        if not node:
            return

        # Si es una hoja (operando)
        if not node.left and not node.right:
            if node.value.isdigit():
                node.type = 'int'
            elif node.value in self.symbol_table:
                node.type = self.symbol_table[node.value]
            else:
                node.type = f'ERROR: Var \'{node.value}\' no declarada'
            return

        # Recorrer recursivamente los hijos primero
        self._annotate_tree(node.left)
        self._annotate_tree(node.right)

        # --- Reglas de compatibilidad de tipos ---
        left_type = node.left.type
        right_type = node.right.type
        op = node.value

        if op in ['*', '/']:
            if 'ERROR' in left_type or 'ERROR' in right_type:
                node.type = 'ERROR: Operando inválido'
            elif left_type == 'int' and right_type == 'int':
                node.type = 'int'
            # Podríamos añadir más reglas (ej. int * real -> real)
            else:
                node.type = f'ERROR: Tipos incompatibles para \'{op}\' ({left_type}, {right_type})'
        
        elif op in ['+', '-']:
            if 'ERROR' in left_type or 'ERROR' in right_type:
                node.type = 'ERROR: Operando inválido'
            elif left_type == 'int' and right_type == 'int':
                node.type = 'int'
            elif left_type == 'real' and right_type == 'int':
                node.type = 'real' # Promoción de tipo
            elif left_type == 'int' and right_type == 'real':
                node.type = 'real' # Promoción de tipo
            else:
                node.type = f'ERROR: Tipos incompatibles para \'{op}\' ({left_type}, {right_type})'
        
        elif op == ':=':
            if 'ERROR' in left_type or 'ERROR' in right_type:
                node.type = 'ERROR: Operando inválido'
            # Regla de asignación: el tipo de la derecha debe ser compatible con el de la izquierda
            elif left_type == right_type or (left_type == 'real' and right_type == 'int'):
                node.type = left_type # La asignación no tiene tipo propio, pero la validamos
            else:
                node.type = f'ERROR: No se puede asignar tipo {right_type} a {left_type}'

    def _generate_markdown(self):
        """Genera el reporte Markdown con el árbol semántico anotado."""
        md = "## 1.3. Análisis Semántico\n\n"
        md += "Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.\n\n"
        md += "```mermaid\n"
        md += "graph TD\n"
        md += "    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;\n"
        md += "    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;\n"
        
        # Función interna para recorrer el árbol y generar las líneas de Mermaid
        def traverse(node):
            lines = []
            node_type = node.type if node.type else " indefinido"
            label = f'["<b>{node.value}</b><br/><i>{node_type}</i>"]'
            style = "error" if "ERROR" in node_type else "default"
            lines.append(f"    {node.id}{label}:::{style}")

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

## `compiler\syntactic_checking.py`

```python
# compiler/syntax_analyzer.py

from .structures import Node

class SyntacticChecking:
    """Construye el árbol de derivación y genera un reporte."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def analyze(self):
        """Realiza el análisis y devuelve el árbol y el reporte."""
        parse_tree = self._parse()
        report = self._generate_markdown(parse_tree)
        return parse_tree, report

    def _current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def _consume(self, expected_type=None):
        kind, val = self._current_token()
        if expected_type and kind != expected_type:
            # El mensaje de error ahora es más informativo
            raise ValueError(f"Error de sintaxis: Se esperaba {expected_type} pero se encontró {kind} ('{val}')")
        self.pos += 1
        return kind, val

    def _parse(self):
        # La gramática sigue siendo S -> ID := E
        root = Node("S")
        
        id_val = self._consume('ID')[1]
        id_node = Node("ID")
        id_node.add_child(Node(id_val))
        root.add_child(id_node)

        # --- CAMBIO CLAVE ---
        # Ahora esperamos 'OPERADOR_ASIGNACION' en lugar de 'ASSIGN'
        assign_val = self._consume('OPERADOR_ASIGNACION')[1]
        root.add_child(Node(assign_val))
        
        root.add_child(self._e())

        if self._current_token()[0] != 'EOF':
            raise ValueError("Error de sintaxis: Tokens extra al final de la expresión.")
        return root
    
    def _e(self):
        node_e = Node("E")
        node_e.add_child(self._t())
        # --- CAMBIO CLAVE ---
        # Ahora comprobamos si el token es de tipo 'OPERADOR_ARITMETICO'
        while self._current_token()[0] == 'OPERADOR_ARITMETICO' and self._current_token()[1] in ('+', '-'):
            op_val = self._consume('OPERADOR_ARITMETICO')[1]
            parent_e = Node("E")
            parent_e.add_child(node_e)
            parent_e.add_child(Node(op_val))
            parent_e.add_child(self._t())
            node_e = parent_e
        return node_e

    def _t(self):
        node_t = Node("T")
        node_t.add_child(self._f())
        # --- CAMBIO CLAVE ---
        # Ahora comprobamos si el token es de tipo 'OPERADOR_ARITMETICO'
        while self._current_token()[0] == 'OPERADOR_ARITMETICO' and self._current_token()[1] in ('*', '/'):
            op_val = self._consume('OPERADOR_ARITMETICO')[1]
            parent_t = Node("T")
            parent_t.add_child(node_t)
            parent_t.add_child(Node(op_val))
            parent_t.add_child(self._f())
            node_t = parent_t
        return node_t

    def _f(self):
        kind, val = self._current_token()
        node_f = Node("F")
        if val == '(':
            self._consume('PAREN')
            node_f.add_child(self._e())
            self._consume('PAREN')
        elif kind == 'ID':
            self._consume('ID')
            id_node = Node("ID")
            id_node.add_child(Node(val))
            node_f.add_child(id_node)
        # --- CAMBIO CLAVE ---
        # Ahora esperamos 'NUMERO_ENTERO' en lugar de 'NUM'
        elif kind == 'NUMERO_ENTERO':
            self._consume('NUMERO_ENTERO')
            num_node = Node("NUM") # Mantenemos 'NUM' en el árbol por simplicidad gramatical
            num_node.add_child(Node(val))
            node_f.add_child(num_node)
        else:
            raise ValueError(f"Sintaxis inválida, se esperaba ID, NUMERO_ENTERO o '(', se encontró {kind}")
        return node_f

    def _generate_markdown(self, root_node):
        # (El código de esta función no necesita cambios)
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
# compiler/syntax_analyzer.py

import re

# --- Definiciones de Operadores ---
precedence = {
    ':=': 0,
    '+': 1, '-': 1,
    '*': 2, '/': 2
}
associativity = {
    ':=': 'right',
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
            if kind in ['ID', 'NUMERO_ENTERO']:
                output.append(value)
            elif value in precedence: # Es un operador
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
                stack.pop() # Quitar '(' de la pila
        
        while stack:
            output.append(stack.pop())
        return output

    def _build_tree(self, postfix_tokens):
        """Construye el AST a partir de una lista de tokens postfijos."""
        stack = []
        operators = precedence.keys()
        
        for token in postfix_tokens:
            if token in operators:
                if len(stack) < 2:
                    raise ValueError(f"Error de sintaxis: Operador '{token}' sin suficientes operandos.")
                right = stack.pop()
                left = stack.pop()
                stack.append(Node(token, left, right))
            else: # Es un operando
                stack.append(Node(token))
        
        if not stack:
             raise ValueError("Error de sintaxis: Expresión vacía o inválida.")
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
                lines.append(f"    {node.id}(('{node.value}'))") # Círculo para operadores
            else:
                lines.append(f"    {node.id}(('{node.value}'))") # Rectángulo para operandos
            
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

