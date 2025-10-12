# compiler/structures.py

import itertools

class Node:
    """Estructura de datos para un nodo del árbol sintáctico."""
    # Usamos un generador global simple para los IDs
    id_counter = itertools.count()

    def __init__(self, symbol):
        self.id = f"n{next(self.id_counter)}"
        self.symbol = symbol
        self.children = []

    def add_child(self, child):
        if child:
            self.children.append(child)