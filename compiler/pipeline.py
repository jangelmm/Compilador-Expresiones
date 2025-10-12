# compiler/pipeline.py

from .lexical_analyzer import LexicalAnalyzer
from .syntax_analizer import SyntaxAnalyzer
from .syntactic_checking import SyntacticChecking
from .intermediate_code_gen import IntermediateCodeGenerator

class CompilationPipeline:
    """Clase principal que gestiona todo el proceso de compilación."""
    def __init__(self, expression):
        self.expression = expression
        self.report = f"# Reporte de Compilación para la Expresión\n\n`{expression}`\n\n---\n"

    def run(self):
        self.report += "\n# Fase 1: Análisis\n";

        """Ejecuta todas las fases del análisis y la síntesis."""
        print("Iniciando Fase 1.1: Análisis Lexicográfico...")
        lex_analyzer = LexicalAnalyzer(self.expression)
        tokens, lex_report = lex_analyzer.analyze()
        self.report += lex_report + "\n---\n"

        self.report += "\n## Fase 1.2: Análisis Sintáctico\n";

        print("Iniciando Fase 1.2.1: Generación de Árbol de Expresión...")
        syntax_analyzer = SyntaxAnalyzer(list(tokens))
        ast_root, syntax_report = syntax_analyzer.analyze()
        self.report += syntax_report + "\n---\n"

        print("Iniciando Fase 1.2.2: Generación de Árbol de Tipos...")
        sc_analizer = SyntacticChecking(list(tokens))
        _, sc_report = sc_analizer.analyze()
        self.report += sc_report + "\n---\n"

        self.report += "\n# Fase 2: Síntesis\n";

        print("Iniciando Fase 2.1: Generación de Código Intermedio...")
        icg = IntermediateCodeGenerator(ast_root)
        icg_report = icg.generate()
        self.report += icg_report

    def save_report(self, filename="reports/reporte_compilacion.md"):
        """Guarda el reporte completo en un archivo .md."""
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.report)
        print(f"\n ¡Reporte guardado exitosamente en '{filename}'!")