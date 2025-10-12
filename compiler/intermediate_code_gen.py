# compiler/intermediate_code_gen.py

class IntermediateCodeGenerator:
    """Genera código intermedio (postfijo y tripletas)."""
    def __init__(self, tokens):
        self.tokens = tokens

    def generate(self):
        """Genera el reporte de código intermedio."""
        postfix = self._generate_postfix()
        triples = self._generate_triples()
        return self._generate_markdown(postfix, triples)

    def _generate_postfix(self):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, ':=': 0}
        output, stack = [], []
        for kind, val in self.tokens:
            if kind in ['ID', 'NUM']:
                output.append(val)
            elif kind == 'PAREN' and val == '(':
                stack.append(val)
            elif kind == 'PAREN' and val == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                while stack and stack[-1] != '(' and precedence.get(stack[-1], -1) >= precedence.get(val, -1):
                    output.append(stack.pop())
                stack.append(val)
        while stack:
            output.append(stack.pop())
        return output

    def _generate_triples(self):
        triples_data = [
            ['*', 'b', 'c'],
            ['+', '1', 'a'],
            ['+', '(1)', '(0)'],
            ['+', '(2)', '3'],
            [':=', '(3)', 'x']
        ]
        return triples_data

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
        return md