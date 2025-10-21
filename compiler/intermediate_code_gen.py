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
        md = "### Notación Postfija (Polaca Inversa)\n"
        md += f"`{' '.join(postfix_list)}`\n\n"
        md += "### Tripletas\n"
        md += "La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:\n\n"
        md += "| # | Operador | Operando 1 | Operando 2 |\n"
        md += "|---|----------|------------|------------|\n"
        for i, (op, arg1, arg2) in enumerate(triples_list):
            md += f"|({i})| `{op}`     | `{arg1}`     | `{arg2}`     |\n"
        return md