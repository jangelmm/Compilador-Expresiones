# main.py

from compiler.pipeline import CompilationPipeline
from compiler.symbol_tables import VariableSymbolTable
import sys
import os

def compile_pascal_file(file_path):
    """Compila un archivo Pascal completo"""
    print(f"\n{'='*60}")
    print(f"COMPILANDO ARCHIVO PASCAL: {file_path}")
    print(f"{'='*60}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        # Inicializar tabla de símbolos VACÍA - se llenará con las declaraciones
        symbol_table = VariableSymbolTable()
        
        pipeline = CompilationPipeline(code, symbol_table)
        pipeline.run()
        
        # Guardar reporte con nombre del archivo
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        report_name = f"reports/reporte_{base_name}.md"
        pipeline.save_report(report_name)
        
        print(f"  Compilación exitosa: {file_path}")
        print(f"  Reporte guardado en: {report_name}")
        
    except Exception as e:
        print(f"  ERROR durante la compilación: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo archivo: python main.py archivo.pas
        file_path = sys.argv[1]
        compile_pascal_file(file_path)
    else:
        # Modo de prueba con código Pascal completo
        pascal_code = """
        program Prueba;
        var
          x, y : integer;
          flag : boolean;
        
        begin
          x := 10;
          y := 5;
          flag := (x > 5) and (y < 10);
        end.
        """
        
        print("Modo de prueba: Compilando código Pascal de ejemplo")
        symbol_table = VariableSymbolTable()
        
        try:
            pipeline = CompilationPipeline(pascal_code, symbol_table)
            pipeline.run()
            pipeline.save_report("reports/reporte_prueba.md")
            print("  Compilación de prueba exitosa!")
        except Exception as e:
            print(f" Error en compilación de prueba: {e}")