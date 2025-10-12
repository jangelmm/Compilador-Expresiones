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
        return md