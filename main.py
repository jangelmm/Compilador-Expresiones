# main.py

from compiler.pipeline import CompilationPipeline

if __name__ == "__main__":
    expression_a_evaluar = "x := 1 + a + (b * c) + 3"

    # Define una tabla de símbolos de ejemplo para la prueba
    tabla_de_simbolos_ejemplo = {
        'x': 'int',
        'a': 'int',
        'b': 'int',
        'c': 'int'
    }
    
    # --- CAMBIO CLAVE AQUÍ ---
    # Pasamos la tabla de símbolos al crear el pipeline
    pipeline = CompilationPipeline(expression_a_evaluar, tabla_de_simbolos_ejemplo)
    
    try:
        pipeline.run()
        pipeline.save_report()
    except ValueError as e:
        print(f"\n ERROR DURANTE LA COMPILACIÓN: {e}")