# Reporte de Compilación para la Expresión

`x := 1 + a + (b * c) + 3`

---

# Fase 1: Análisis
## 1.1. Análisis Lexicográfico

El código fuente se descompone en los siguientes tokens:

| Tipo | Valor | ID |
|------|-------|----|
| IDENTIFIER | `x` | 10875 |
| OPERATOR | `:=` | 101 |
| CONSTANT | `1` | None |
| OPERATOR | `+` | 102 |
| IDENTIFIER | `a` | 10688 |
| OPERATOR | `+` | 102 |
| PAREN | `(` | None |
| IDENTIFIER | `b` | 10991 |
| OPERATOR | `*` | 104 |
| IDENTIFIER | `c` | 10908 |
| PAREN | `)` | None |
| OPERATOR | `+` | 102 |
| CONSTANT | `3` | None |

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
| 10875 | x | integer | 0 | 1000 | direct |
| 10688 | a | integer | 0 | 1004 | direct |
| 10991 | b | integer | 0 | 1008 | direct |
| 10908 | c | integer | 0 | 100C | direct |

**Total de símbolos:** 4
**Siguiente dirección disponible:** 1010

---

## Fase 1.2: Análisis Sintáctico
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `x 1 a + b c * + 3 + :=`

```mermaid
graph TD
    N10((':='))
    N0(['x'])
    N10 --> N0
    N9(('+'))
    N7(('+'))
    N3(('+'))
    N1(['1'])
    N3 --> N1
    N2(['a'])
    N3 --> N2
    N7 --> N3
    N6(('*'))
    N4(['b'])
    N6 --> N4
    N5(['c'])
    N6 --> N5
    N7 --> N6
    N9 --> N7
    N8(['3'])
    N9 --> N8
    N10 --> N9
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n0['S'] --- n1['ID']
    n0['S'] --- n3[':=']
    n0['S'] --- n23['F']
    n1['ID'] --- n2['x']
    n23['F'] --- n12['F']
    n23['F'] --- n24['+']
    n23['F'] --- n25['I']
    n12['F'] --- n7['F']
    n12['F'] --- n13['+']
    n12['F'] --- n14['I']
    n25['I'] --- n26['NUM']
    n7['F'] --- n4['I']
    n7['F'] --- n8['+']
    n7['F'] --- n9['I']
    n14['I'] --- n18['G']
    n26['NUM'] --- n27['3']
    n4['I'] --- n5['NUM']
    n9['I'] --- n10['ID']
    n18['G'] --- n15['I']
    n18['G'] --- n19['*']
    n18['G'] --- n20['I']
    n5['NUM'] --- n6['1']
    n10['ID'] --- n11['a']
    n15['I'] --- n16['ID']
    n20['I'] --- n21['ID']
    n16['ID'] --- n17['b']
    n21['ID'] --- n22['c']
```

---
## 1.3. Análisis Semántico

Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.

```mermaid
graph TD
    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;
    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;
    classDef immediate fill:#ddddff,stroke:#44d,stroke-width:2px;
    N10["<b>:=</b><br/><i>integer</i><br/>Modo: direct"]:::default
    N0["<b>x</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1000"]:::default
    N10 --> N0
    N9["<b>+</b><br/><i>integer</i><br/>Modo: register"]:::default
    N7["<b>+</b><br/><i>integer</i><br/>Modo: register"]:::default
    N3["<b>+</b><br/><i>integer</i><br/>Modo: register"]:::default
    N1["<b>1</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N3 --> N1
    N2["<b>a</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1004"]:::default
    N3 --> N2
    N7 --> N3
    N6["<b>*</b><br/><i>integer</i><br/>Modo: register"]:::default
    N4["<b>b</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1008"]:::default
    N6 --> N4
    N5["<b>c</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 100C"]:::default
    N6 --> N5
    N7 --> N6
    N9 --> N7
    N8["<b>3</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N9 --> N8
    N10 --> N9
```

### Resumen de Tipos en la Expresión

- **integer**: 11 ocurrencias

---

# Fase 2: Síntesis
## 3. Representación Intermedia

### Notación Postfija (Polaca Inversa)
`x 1 a + b c * + 3 + :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `+`     | `1`     | `a`     |
|(1)| `*`     | `b`     | `c`     |
|(2)| `+`     | `(0)`     | `(1)`     |
|(3)| `+`     | `(2)`     | `3`     |
|(4)| `:=`     | `x`     | `(3)`     |
