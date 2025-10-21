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

        md += "\n" + TypeSystem.get_operator_tables_markdown(['+', '*']) + "\n"
        
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
        
        return md