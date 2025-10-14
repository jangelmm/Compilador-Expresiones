# Reporte de Compilación para la Expresión

`flag := (x > 5) and (y < 10)`

---

# Fase 1: Análisis
## 1.1. Análisis Lexicográfico

El código fuente se descompone en los siguientes tokens:

| Tipo | Valor | ID |
|------|-------|----|
| IDENTIFIER | `flag` | 10926 |
| OPERATOR | `:=` | 101 |
| PAREN | `(` | None |
| IDENTIFIER | `x` | 10520 |
| OPERATOR | `>` | 108 |
| CONSTANT | `5` | None |
| PAREN | `)` | None |
| IDENTIFIER | `and` | 10423 |
| PAREN | `(` | None |
| IDENTIFIER | `y` | 10645 |
| OPERATOR | `<` | 107 |
| CONSTANT | `10` | None |
| PAREN | `)` | None |

---
## Tablas Fijas del Lenguaje

### Palabras Reservadas
| ID | Palabra |
|----|---------|
| 1 | var |
| 2 | proc |
| 3 | begin |
| 4 | end |
| 5 | integer |
| 6 | char |
| 7 | real |

### Operadores
| ID | Operador |
|----|----------|
| 101 | := |
| 102 | + |
| 103 | - |
| 104 | * |
| 105 | / |
| 106 | = |
| 107 | < |
| 108 | > |
| 109 | <= |
| 110 | >= |
| 111 | <> |
| 112 | and |
| 113 | or |
| 114 | not |

### Delimitadores
| ID | Delimitador |
|----|-------------|
| 201 | : |
| 202 | ; |
| 203 | ( |
| 204 | ) |

## Tabla de Símbolos Variables

| ID | Nombre | Tipo | Scope | Dirección | Modo |
|----|--------|------|-------|-----------|------|
| 10926 | flag | boolean | 0 | 1000 | direct |
| 10520 | x | integer | 0 | 1004 | direct |
| 10645 | y | integer | 0 | 1008 | direct |
| 10423 | and | integer | 0 | 100C | direct |

**Total de símbolos:** 4
**Siguiente dirección disponible:** 1010

---

## Fase 1.2: Análisis Sintáctico
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `flag x 5 > and y 10 < :=`

```mermaid
graph TD
    N8((':='))
    N4(('and'))
    N0(['flag'])
    N4 --> N0
    N3(('>'))
    N1(['x'])
    N3 --> N1
    N2(['5'])
    N3 --> N2
    N4 --> N3
    N8 --> N4
    N7(('<'))
    N5(['y'])
    N7 --> N5
    N6(['10'])
    N7 --> N6
    N8 --> N7
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

**Error de sintaxis:** Error de sintaxis: Tokens extra al final de la expresión: ('IDENTIFIER', 'and')

La secuencia de tokens no pudo ser validada completamente por la gramática.

---
## 1.3. Análisis Semántico

Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.

```mermaid
graph TD
    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;
    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;
    classDef immediate fill:#ddddff,stroke:#44d,stroke-width:2px;
    N8["<b>:=</b><br/><i>boolean</i><br/>Modo: direct"]:::default
    N4["<b>and</b><br/><i>boolean</i><br/>Modo: register"]:::default
    N0["<b>flag</b><br/><i>boolean</i><br/>Modo: direct<br/>Addr: 1000"]:::default
    N4 --> N0
    N3["<b>></b><br/><i>boolean</i><br/>Modo: register"]:::default
    N1["<b>x</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1004"]:::default
    N3 --> N1
    N2["<b>5</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N3 --> N2
    N4 --> N3
    N8 --> N4
    N7["<b><</b><br/><i>boolean</i><br/>Modo: register"]:::default
    N5["<b>y</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1008"]:::default
    N7 --> N5
    N6["<b>10</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N7 --> N6
    N8 --> N7
```

### Resumen de Tipos en la Expresión

- **boolean**: 5 ocurrencias
- **integer**: 4 ocurrencias

---

# Fase 2: Síntesis
## 3. Representación Intermedia

### Notación Postfija (Polaca Inversa)
`flag x 5 > and y 10 < :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `>`     | `x`     | `5`     |
|(1)| `and`     | `flag`     | `(0)`     |
|(2)| `<`     | `y`     | `10`     |
|(3)| `:=`     | `(1)`     | `(2)`     |
