# compiler/syntax_analyzer.py

from .structures import Node

class SemanticAnalizer:
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
        md = "## 1.3. Análisis Semántico\n\n"
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
        return md