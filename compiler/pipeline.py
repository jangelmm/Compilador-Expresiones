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
        print(f"\n ¡Reporte guardado exitosamente en '{filename}'!")