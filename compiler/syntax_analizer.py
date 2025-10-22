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
        md = "La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.\n\n"
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
        return md