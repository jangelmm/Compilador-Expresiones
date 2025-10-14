# Reporte de Compilación para la Expresión

`result := 3.14 * radius + 2.5`

---

# Fase 1: Análisis
## 1.1. Análisis Lexicográfico

El código fuente se descompone en los siguientes tokens:

| Tipo | Valor | ID |
|------|-------|----|
| IDENTIFIER | `result` | 10721 |
| OPERATOR | `:=` | 101 |
| CONSTANT | `3.14` | None |
| OPERATOR | `*` | 104 |
| IDENTIFIER | `radius` | 10610 |
| OPERATOR | `+` | 102 |
| CONSTANT | `2.5` | None |

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
| 10721 | result | real | 0 | 1000 | direct |
| 10610 | radius | real | 0 | 1004 | direct |

**Total de símbolos:** 2
**Siguiente dirección disponible:** 1008

---

## Fase 1.2: Análisis Sintáctico
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `result 3.14 radius * 2.5 + :=`

```mermaid
graph TD
    N6((':='))
    N0(['result'])
    N6 --> N0
    N5(('+'))
    N3(('*'))
    N1(['3.14'])
    N3 --> N1
    N2(['radius'])
    N3 --> N2
    N5 --> N3
    N4(['2.5'])
    N5 --> N4
    N6 --> N5
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n0['S'] --- n1['ID']
    n0['S'] --- n3[':=']
    n0['S'] --- n12['F']
    n1['ID'] --- n2['result']
    n12['F'] --- n7['G']
    n12['F'] --- n13['+']
    n12['F'] --- n14['I']
    n7['G'] --- n4['I']
    n7['G'] --- n8['*']
    n7['G'] --- n9['I']
    n14['I'] --- n15['NUM']
    n4['I'] --- n5['NUM']
    n9['I'] --- n10['ID']
    n15['NUM'] --- n16['2.5']
    n5['NUM'] --- n6['3.14']
    n10['ID'] --- n11['radius']
```

---
## 1.3. Análisis Semántico

Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.

```mermaid
graph TD
    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;
    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;
    classDef immediate fill:#ddddff,stroke:#44d,stroke-width:2px;
    N6["<b>:=</b><br/><i>real</i><br/>Modo: direct"]:::default
    N0["<b>result</b><br/><i>real</i><br/>Modo: direct<br/>Addr: 1000"]:::default
    N6 --> N0
    N5["<b>+</b><br/><i>real</i><br/>Modo: register"]:::default
    N3["<b>*</b><br/><i>real</i><br/>Modo: register"]:::default
    N1["<b>3.14</b><br/><i>real</i><br/>Modo: immediate"]:::immediate
    N3 --> N1
    N2["<b>radius</b><br/><i>real</i><br/>Modo: direct<br/>Addr: 1004"]:::default
    N3 --> N2
    N5 --> N3
    N4["<b>2.5</b><br/><i>real</i><br/>Modo: immediate"]:::immediate
    N5 --> N4
    N6 --> N5
```

### Resumen de Tipos en la Expresión

- **real**: 7 ocurrencias

---

# Fase 2: Síntesis
## 3. Representación Intermedia

### Notación Postfija (Polaca Inversa)
`result 3.14 radius * 2.5 + :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `*`     | `3.14`     | `radius`     |
|(1)| `+`     | `(0)`     | `2.5`     |
|(2)| `:=`     | `result`     | `(1)`     |
