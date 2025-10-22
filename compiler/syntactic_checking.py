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
            # Si hay error, generar un reporte de error (sin título duplicado)
            error_report = f"**Error de sintaxis:** {str(e)}\n\n"
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
        md = "La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:\n\n"
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