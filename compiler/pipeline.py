# compiler/pipeline.py

from .lexical_analyzer import LexicalAnalyzer
from .syntax_analizer import SyntaxAnalyzer
from .syntactic_checking import SyntacticChecking
from .semantic_analyzer import SemanticAnalyzer
from .intermediate_code_gen import IntermediateCodeGenerator
from .declaration_analyzer import DeclarationAnalyzer
from .symbol_tables import generate_fixed_tables_report

class CompilationPipeline:
    def __init__(self, code_string, symbol_table=None):
        self.code = code_string
        self.symbol_table = symbol_table
        self.report = f"# Reporte de Compilación\n\n```pascal\n{code_string}\n```\n\n---\n"

    def run(self):
        """Ejecuta el pipeline completo de compilación."""
        
        # FASE 0: Análisis de Declaraciones (CREA la tabla de símbolos variables)
        self.report += "\n# Fase 0: Análisis de Declaraciones\n"
        print("Iniciando Fase 0: Análisis de Declaraciones...")
        
        declaration_analyzer = DeclarationAnalyzer(self.symbol_table)
        self.symbol_table = declaration_analyzer.analyze_declarations(self.code)
        
        self.report += "\n## Tabla de Símbolos Variables (Declaradas)\n\n"
        self.report += self.symbol_table.generate_markdown_report() + "\n---\n"

        # FASE 1: Análisis
        self.report += "\n# Fase 1: Análisis\n"

        print("Iniciando Fase 1.1: Análisis Lexicográfico...")
        lex_analyzer = LexicalAnalyzer(self.code, self.symbol_table)
        tokens, lex_report = lex_analyzer.analyze()
        self.report += lex_report + "\n---\n"

        # Verificar variables no declaradas
        undeclared = declaration_analyzer.get_undeclared_variables(tokens)
        if undeclared:
            self.report += "\n## Variables No Declaradas\n\n"
            for var in undeclared:
                self.report += f"- `{var}`\n"
            self.report += "\n---\n"
            raise ValueError(f"Variables no declaradas: {', '.join(undeclared)}")

        # AGREGAR reportes de tablas fijas
        self.report += generate_fixed_tables_report() + "\n---\n"

        # Extraer solo las sentencias ejecutables (después del 'begin')
        executable_tokens = self._extract_executable_tokens(tokens)
        
        if not executable_tokens:
            raise ValueError("No se encontraron sentencias ejecutables después del 'begin'")

        self.report += "\n## Fase 1.2: Análisis Sintáctico\n"

        # Procesar cada sentencia por separado
        for i, stmt_tokens in enumerate(executable_tokens):
            self.report += f"\n### Sentencia {i+1}\n"
            
            print(f"Iniciando Fase 1.2.1: Generación de Árbol de Expresión para sentencia {i+1}...")
            syntax_tokens = [(kind, value) for kind, value, _ in stmt_tokens]
            syntax_analyzer = SyntaxAnalyzer(syntax_tokens)
            ast_root, syntax_report = syntax_analyzer.analyze()
            self.report += syntax_report + "\n---\n"

            print(f"Iniciando Fase 1.2.2: Comprobación Sintáctica para sentencia {i+1}...")
            sc_analizer = SyntacticChecking(syntax_tokens)
            parse_tree, sc_report = sc_analizer.analyze()
            self.report += sc_report + "\n---\n"

            print(f"Iniciando Fase 1.3: Análisis Semántico para sentencia {i+1}...")
            semantic_analyzer = SemanticAnalyzer(ast_root, self.symbol_table)
            annotated_ast, semantic_report = semantic_analyzer.analyze()
            self.report += semantic_report + "\n---\n"

            self.report += "\n# Fase 2: Síntesis\n"

            print(f"Iniciando Fase 2.1: Generación de Código Intermedio para sentencia {i+1}...")
            icg = IntermediateCodeGenerator(annotated_ast)
            icg_report = icg.generate()
            self.report += icg_report

    def _extract_executable_tokens(self, tokens):
        """
        Extrae las sentencias ejecutables del bloque BEGIN-END.
        Retorna una lista de listas de tokens, donde cada lista interna es una sentencia.
        """
        # Encontrar el inicio del bloque BEGIN
        begin_index = -1
        for i, (token_type, value, _) in enumerate(tokens):
            if token_type == 'RESERVED_WORD' and value.lower() == 'begin':
                begin_index = i + 1
                break
        
        if begin_index == -1:
            return []
        
        # Encontrar el final del bloque END
        end_index = -1
        for i in range(begin_index, len(tokens)):
            token_type, value, _ = tokens[i]
            if token_type == 'RESERVED_WORD' and value.lower() == 'end':
                end_index = i
                break
        
        if end_index == -1:
            end_index = len(tokens)
        
        # Extraer tokens entre BEGIN y END
        executable_tokens = tokens[begin_index:end_index]
        
        # Dividir en sentencias individuales (separadas por ';')
        statements = []
        current_statement = []
        
        for token in executable_tokens:
            token_type, value, table_id = token
            
            # Si encontramos un punto y coma, terminar la sentencia actual
            if token_type == 'DELIMITER' and value == ';':
                if current_statement:  # Solo agregar si hay tokens
                    statements.append(current_statement)
                    current_statement = []
            else:
                current_statement.append(token)
        
        # Agregar la última sentencia si existe
        if current_statement:
            statements.append(current_statement)
        
        return statements

    def save_report(self, filename="reports/reporte_compilacion.md"):
        import os
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self.report)
        print(f"\n ¡Reporte guardado exitosamente en '{filename}'!")