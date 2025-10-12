# Reporte de Compilación para la Expresión

`x := 1 + a + (b * c) + 3`

---

# Fase 1: Análisis
## 1.1. Análisis Lexicográfico

El código fuente se descompone en los siguientes tokens:

| Tipo                    | Valor         |
|-------------------------|---------------|
| ID                      | `x`      |
| OPERADOR_ASIGNACION     | `:=`      |
| NUMERO_ENTERO           | `1`      |
| OPERADOR_ARITMETICO     | `+`      |
| ID                      | `a`      |
| OPERADOR_ARITMETICO     | `+`      |
| PAREN                   | `(`      |
| ID                      | `b`      |
| OPERADOR_ARITMETICO     | `*`      |
| ID                      | `c`      |
| PAREN                   | `)`      |
| OPERADOR_ARITMETICO     | `+`      |
| NUMERO_ENTERO           | `3`      |

---
## 1.2. Análisis Sintáctico (AST)

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `x 1 a + b c * + 3 + :=`

```mermaid
graph TD
    N10((':='))
    N0(('x'))
    N10 --> N0
    N9(('+'))
    N7(('+'))
    N3(('+'))
    N1(('1'))
    N3 --> N1
    N2(('a'))
    N3 --> N2
    N7 --> N3
    N6(('*'))
    N4(('b'))
    N6 --> N4
    N5(('c'))
    N6 --> N5
    N7 --> N6
    N9 --> N7
    N8(('3'))
    N9 --> N8
    N10 --> N9
```

---
## 1.3. Análisis Semántico

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n0['S'] --- n1['ID']
    n0['S'] --- n3[':=']
    n0['S'] --- n29['E']
    n1['ID'] --- n2['x']
    n29['E'] --- n15['E']
    n29['E'] --- n30['+']
    n29['E'] --- n31['T']
    n15['E'] --- n9['E']
    n15['E'] --- n16['+']
    n15['E'] --- n17['T']
    n31['T'] --- n32['F']
    n9['E'] --- n4['E']
    n9['E'] --- n10['+']
    n9['E'] --- n11['T']
    n17['T'] --- n18['F']
    n32['F'] --- n33['NUM']
    n4['E'] --- n5['T']
    n11['T'] --- n12['F']
    n18['F'] --- n19['E']
    n33['NUM'] --- n34['3']
    n5['T'] --- n6['F']
    n12['F'] --- n13['ID']
    n19['E'] --- n24['T']
    n6['F'] --- n7['NUM']
    n13['ID'] --- n14['a']
    n24['T'] --- n20['T']
    n24['T'] --- n25['*']
    n24['T'] --- n26['F']
    n7['NUM'] --- n8['1']
    n20['T'] --- n21['F']
    n26['F'] --- n27['ID']
    n21['F'] --- n22['ID']
    n27['ID'] --- n28['c']
    n22['ID'] --- n23['b']
```

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
