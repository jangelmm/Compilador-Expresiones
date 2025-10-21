# compiler/pipeline.py

from .parser import Parser
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
        self.report = "# Proceso de Compilación\n\n"
        self.report += f"**Expresión:** `{expression}`\n\n"
        self.report += "---\n"

    def run(self):
        # Fase 1: Parseo
        self.report += "\n"
        print("Iniciando Fase 1: Parseo...")
        parser = Parser(self.expression)
        lexemes = parser.parse()
        self.report += parser.generate_markdown() + "\n"

        # Fase 2: Análisis Lexicográfico
        self.report += "\n"
        print("Iniciando Fase 2: Análisis Lexicográfico...")
        lex_analyzer = LexicalAnalyzer(lexemes, self.symbol_table)
        tokens, lex_report = lex_analyzer.analyze()
        self.report += lex_report + "\n"

        # Fase 3: Análisis Sintáctico
        self.report += "\n## 3. Análisis Sintáctico\n\n"
        print("Iniciando Fase 3: Análisis Sintáctico...")

        # 3.1 Generación de Árbol de Expresión (AST)
        print("Iniciando Fase 3.1: Generación de Árbol de Expresión...")
        syntax_tokens = [(kind, value) for kind, value, _ in tokens]
        syntax_analyzer = SyntaxAnalyzer(syntax_tokens)
        ast_root, syntax_report = syntax_analyzer.analyze()
        self.report += syntax_report + "\n"

        # 3.2 Comprobación Sintáctica (Árbol de Derivación)
        print("Iniciando Fase 3.2: Comprobación Sintáctica...")
        sc_analizer = SyntacticChecking(syntax_tokens)
        parse_tree, sc_report = sc_analizer.analyze()
        self.report += sc_report + "\n"

        # Fase 4: Análisis Semántico
        self.report += "\n## 4. Análisis Semántico\n\n"
        print("Iniciando Fase 4: Análisis Semántico...")
        semantic_analyzer = SemanticAnalyzer(ast_root, lex_analyzer.symbol_table)
        annotated_ast, semantic_report = semantic_analyzer.analyze()
        self.report += semantic_report + "\n"

        # Fase 5: Síntesis (Generación de Código Intermedio)
        self.report += "\n## 5. Síntesis (Generación de Código Intermedio)\n\n"
        print("Iniciando Fase 5: Generación de Código Intermedio...")
        icg = IntermediateCodeGenerator(annotated_ast)
        icg_report = icg.generate()
        self.report += icg_report

        # Conclusión
        self.report += "\n# Conclusión\n\n"
        self.report += "El proceso de compilación consta de **etapas secuenciales**, donde cada una garantiza la corrección del código antes de pasar a la siguiente:\n\n"
        self.report += "| Etapa | Propósito | Ejemplo |\n"
        self.report += "|:------|:----------|:--------|\n"
        self.report += "| **Parseo** | Lee caracteres y forma palabras | `x := 1 + a + (b * c) + 3` |\n"
        self.report += "| **Análisis Léxico** | Clasifica tokens | `ID`, `NUM`, `+`, `*`, `:=` |\n"
        self.report += "| **Análisis Sintáctico** | Verifica reglas gramaticales | Árbol de expresión |\n"
        self.report += "| **Análisis Semántico** | Verifica tipos y operaciones | Error o validación de tipos |\n"
        self.report += "| **Síntesis** | Genera código intermedio | Tripletas o cuádruplas |\n\n"
        self.report += "---\n"

    def save_report(self, filename="reports/reporte_compilacion.md"):
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.report)
        print(f"\n ¡Reporte guardado exitosamente en '{filename}'!")