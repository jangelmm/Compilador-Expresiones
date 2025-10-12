# main.py

from compiler.pipeline import CompilationPipeline

if __name__ == "__main__":
    expression_a_evaluar = "x := 1 + a + (b * c) + 3"
    
    pipeline = CompilationPipeline(expression_a_evaluar)
    try:
        pipeline.run()
        pipeline.save_report()
    except ValueError as e:
        print(f"\n ERROR DURANTE LA COMPILACIÓN: {e}")