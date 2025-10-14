# main.py

from compiler.pipeline import CompilationPipeline
from compiler.symbol_tables import VariableSymbolTable

if __name__ == "__main__":
    # Ejemplo con diferentes tipos
    expressions = [
        # "x := 1 + a + (b * c) + 3",  # Enteros
        # "result := 3.14 * radius + 2.5",  # Reales
        # "message := 'Hola ' + 'Mundo'",  # Strings
        # "flag := (x > 5) and (y < 10)",  # Booleanos
        # "mixed := 10 + 3.14"  # Mixed types
    ]
    
    for expression in expressions:
        print(f"\n{'='*50}")
        print(f"Compilando: {expression}")
        print(f"{'='*50}")
        
        symbol_table = VariableSymbolTable()
        
        # Definir símbolos según la expresión
        if "message :=" in expression:
            symbol_table.add_symbol('message', 'string')
        elif "result :=" in expression:
            symbol_table.add_symbol('result', 'real')
            symbol_table.add_symbol('radius', 'real')
        elif "flag :=" in expression:
            symbol_table.add_symbol('flag', 'boolean')
            symbol_table.add_symbol('x', 'integer')
            symbol_table.add_symbol('y', 'integer')
        elif "mixed :=" in expression:
            symbol_table.add_symbol('mixed', 'real')
        else:
            # Default: enteros
            symbol_table.add_symbol('x', 'integer')
            symbol_table.add_symbol('a', 'integer')
            symbol_table.add_symbol('b', 'integer') 
            symbol_table.add_symbol('c', 'integer')
        
        pipeline = CompilationPipeline(expression, symbol_table)
        
        try:
            pipeline.run()
            pipeline.save_report(f"reports/reporte_{expression.split()[0]}.md")
            print(f" Compilación exitosa para: {expression}")
        except ValueError as e:
            print(f" ERROR: {e}")