# Reporte de Compilación

```pascal
program Ejemplo;
var
  a, b : integer;
  c : real;
  flag : boolean;
  nombre : string;
begin
  a := 10;
  b := 20;
  c := a + b / 2.5;
  flag := (a > 5) and (b < 30);
  nombre := 'Hola Mundo';
end.
```

---

# Fase 0: Análisis de Declaraciones

## Tabla de Símbolos Variables (Declaradas)

## Tabla de Símbolos Variables

| ID | Nombre | Tipo | Scope | Dirección |
|----|--------|------|-------|-----------|
| 10798 | a | integer | 0 | 1000 |
| 10516 | b | integer | 0 | 1004 |
| 10127 | c | real | 0 | 1008 |
| 10370 | flag | boolean | 0 | 100C |
| 10726 | nombre | string | 0 | 1010 |

**Total de símbolos:** 5
**Siguiente dirección disponible:** 1014

---

# Fase 1: Análisis
## 1.1. Análisis Lexicográfico

El código fuente se descompone en los siguientes tokens:

| Token | Lexema | ID Tabla |
|-------|--------|----------|
| RESERVED_WORD | `program` | 8 |
| PROGRAM_NAME | `ejemplo` | PROGRAM |
| DELIMITER | `;` | 202 |
| RESERVED_WORD | `var` | 1 |
| IDENTIFIER | `a` | 10798 |
| COMMA | `,` | None |
| IDENTIFIER | `b` | 10516 |
| COLON | `:` | None |
| RESERVED_WORD | `integer` | 5 |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `c` | 10127 |
| COLON | `:` | None |
| RESERVED_WORD | `real` | 7 |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `flag` | 10370 |
| COLON | `:` | None |
| RESERVED_WORD | `boolean` | 9 |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `nombre` | 10726 |
| COLON | `:` | None |
| RESERVED_WORD | `string` | 10 |
| DELIMITER | `;` | 202 |
| RESERVED_WORD | `begin` | 3 |
| IDENTIFIER | `a` | 10798 |
| OPERATOR | `:=` | 101 |
| CONSTANT | `10` | None |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `b` | 10516 |
| OPERATOR | `:=` | 101 |
| CONSTANT | `20` | None |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `c` | 10127 |
| OPERATOR | `:=` | 101 |
| IDENTIFIER | `a` | 10798 |
| OPERATOR | `+` | 102 |
| IDENTIFIER | `b` | 10516 |
| OPERATOR | `/` | 105 |
| CONSTANT | `2.5` | None |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `flag` | 10370 |
| OPERATOR | `:=` | 101 |
| PAREN | `(` | None |
| IDENTIFIER | `a` | 10798 |
| OPERATOR | `>` | 108 |
| CONSTANT | `5` | None |
| PAREN | `)` | None |
| OPERATOR | `and` | 112 |
| PAREN | `(` | None |
| IDENTIFIER | `b` | 10516 |
| OPERATOR | `<` | 107 |
| CONSTANT | `30` | None |
| PAREN | `)` | None |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `nombre` | 10726 |
| OPERATOR | `:=` | 101 |
| STRING | `'Hola Mundo'` | None |
| DELIMITER | `;` | 202 |
| RESERVED_WORD | `end` | 4 |
| DELIMITER | `.` | 206 |

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
| 8 | program |
| 9 | boolean |
| 10 | string |

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
| 205 | , |
| 206 | . |

---

## Fase 1.2: Análisis Sintáctico

### Sentencia 1
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `a 10 :=`

```mermaid
graph TD
    N2((':='))
    N0(['a'])
    N2 --> N0
    N1(['10'])
    N2 --> N1
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n0['S'] --- n1['ID']
    n0['S'] --- n3[':=']
    n0['S'] --- n4['I']
    n1['ID'] --- n2['a']
    n4['I'] --- n5['NUM']
    n5['NUM'] --- n6['10']
```

---
## 1.3. Análisis Semántico

Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.

```mermaid
graph TD
    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;
    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;
    classDef immediate fill:#ddddff,stroke:#44d,stroke-width:2px;
    N2["<b>:=</b><br/><i>integer</i><br/>Modo: direct"]:::default
    N0["<b>a</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1000"]:::default
    N2 --> N0
    N1["<b>10</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N2 --> N1
```

### Resumen de Tipos en la Expresión

- **integer**: 3 ocurrencias

---

# Fase 2: Síntesis
## 3. Representación Intermedia

### Notación Postfija (Polaca Inversa)
`a 10 :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `:=`     | `a`     | `10`     |

### Sentencia 2
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `b 20 :=`

```mermaid
graph TD
    N2((':='))
    N0(['b'])
    N2 --> N0
    N1(['20'])
    N2 --> N1
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n7['S'] --- n8['ID']
    n7['S'] --- n10[':=']
    n7['S'] --- n11['I']
    n8['ID'] --- n9['b']
    n11['I'] --- n12['NUM']
    n12['NUM'] --- n13['20']
```

---
## 1.3. Análisis Semántico

Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.

```mermaid
graph TD
    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;
    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;
    classDef immediate fill:#ddddff,stroke:#44d,stroke-width:2px;
    N2["<b>:=</b><br/><i>integer</i><br/>Modo: direct"]:::default
    N0["<b>b</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1004"]:::default
    N2 --> N0
    N1["<b>20</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N2 --> N1
```

### Resumen de Tipos en la Expresión

- **integer**: 3 ocurrencias

---

# Fase 2: Síntesis
## 3. Representación Intermedia

### Notación Postfija (Polaca Inversa)
`b 20 :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `:=`     | `b`     | `20`     |

### Sentencia 3
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `c a b 2.5 / + :=`

```mermaid
graph TD
    N6((':='))
    N0(['c'])
    N6 --> N0
    N5(('+'))
    N1(['a'])
    N5 --> N1
    N4(('/'))
    N2(['b'])
    N4 --> N2
    N3(['2.5'])
    N4 --> N3
    N5 --> N4
    N6 --> N5
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n14['S'] --- n15['ID']
    n14['S'] --- n17[':=']
    n14['S'] --- n21['F']
    n15['ID'] --- n16['c']
    n21['F'] --- n18['I']
    n21['F'] --- n22['+']
    n21['F'] --- n26['G']
    n18['I'] --- n19['ID']
    n26['G'] --- n23['I']
    n26['G'] --- n27['/']
    n26['G'] --- n28['I']
    n19['ID'] --- n20['a']
    n23['I'] --- n24['ID']
    n28['I'] --- n29['NUM']
    n24['ID'] --- n25['b']
    n29['NUM'] --- n30['2.5']
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
    N0["<b>c</b><br/><i>real</i><br/>Modo: direct<br/>Addr: 1008"]:::default
    N6 --> N0
    N5["<b>+</b><br/><i>real</i><br/>Modo: register"]:::default
    N1["<b>a</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1000"]:::default
    N5 --> N1
    N4["<b>/</b><br/><i>real</i><br/>Modo: register"]:::default
    N2["<b>b</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1004"]:::default
    N4 --> N2
    N3["<b>2.5</b><br/><i>real</i><br/>Modo: immediate"]:::immediate
    N4 --> N3
    N5 --> N4
    N6 --> N5
```

### Resumen de Tipos en la Expresión

- **real**: 5 ocurrencias
- **integer**: 2 ocurrencias

---

# Fase 2: Síntesis
## 3. Representación Intermedia

### Notación Postfija (Polaca Inversa)
`c a b 2.5 / + :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `/`     | `b`     | `2.5`     |
|(1)| `+`     | `a`     | `(0)`     |
|(2)| `:=`     | `c`     | `(1)`     |

### Sentencia 4
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `flag a 5 > b 30 < and :=`

```mermaid
graph TD
    N8((':='))
    N0(['flag'])
    N8 --> N0
    N7(('and'))
    N3(('>'))
    N1(['a'])
    N3 --> N1
    N2(['5'])
    N3 --> N2
    N7 --> N3
    N6(('<'))
    N4(['b'])
    N6 --> N4
    N5(['30'])
    N6 --> N5
    N7 --> N6
    N8 --> N7
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n31['S'] --- n32['ID']
    n31['S'] --- n34[':=']
    n31['S'] --- n44['E']
    n32['ID'] --- n33['flag']
    n44['E'] --- n35['I']
    n44['E'] --- n45['and']
    n44['E'] --- n46['I']
    n35['I'] --- n39['T']
    n46['I'] --- n50['T']
    n39['T'] --- n36['I']
    n39['T'] --- n40['>']
    n39['T'] --- n41['I']
    n50['T'] --- n47['I']
    n50['T'] --- n51['<']
    n50['T'] --- n52['I']
    n36['I'] --- n37['ID']
    n41['I'] --- n42['NUM']
    n47['I'] --- n48['ID']
    n52['I'] --- n53['NUM']
    n37['ID'] --- n38['a']
    n42['NUM'] --- n43['5']
    n48['ID'] --- n49['b']
    n53['NUM'] --- n54['30']
```

---
## 1.3. Análisis Semántico

Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.

```mermaid
graph TD
    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;
    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;
    classDef immediate fill:#ddddff,stroke:#44d,stroke-width:2px;
    N8["<b>:=</b><br/><i>boolean</i><br/>Modo: direct"]:::default
    N0["<b>flag</b><br/><i>boolean</i><br/>Modo: direct<br/>Addr: 100C"]:::default
    N8 --> N0
    N7["<b>and</b><br/><i>boolean</i><br/>Modo: register"]:::default
    N3["<b>></b><br/><i>boolean</i><br/>Modo: register"]:::default
    N1["<b>a</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1000"]:::default
    N3 --> N1
    N2["<b>5</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N3 --> N2
    N7 --> N3
    N6["<b><</b><br/><i>boolean</i><br/>Modo: register"]:::default
    N4["<b>b</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1004"]:::default
    N6 --> N4
    N5["<b>30</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N6 --> N5
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
`flag a 5 > b 30 < and :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `>`     | `a`     | `5`     |
|(1)| `<`     | `b`     | `30`     |
|(2)| `and`     | `(0)`     | `(1)`     |
|(3)| `:=`     | `flag`     | `(2)`     |

### Sentencia 5
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `nombre 'Hola Mundo' :=`

```mermaid
graph TD
    N2((':='))
    N0(['nombre'])
    N2 --> N0
    N1([''Hola Mundo''])
    N2 --> N1
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n55['S'] --- n56['ID']
    n55['S'] --- n58[':=']
    n55['S'] --- n59['I']
    n56['ID'] --- n57['nombre']
    n59['I'] --- n60['STRING']
    n60['STRING'] --- n61[''Hola Mundo'']
```

---
## 1.3. Análisis Semántico

Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.

```mermaid
graph TD
    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;
    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;
    classDef immediate fill:#ddddff,stroke:#44d,stroke-width:2px;
    N2["<b>:=</b><br/><i>string</i><br/>Modo: direct"]:::default
    N0["<b>nombre</b><br/><i>string</i><br/>Modo: direct<br/>Addr: 1010"]:::default
    N2 --> N0
    N1["<b>'Hola Mundo'</b><br/><i>char</i><br/>Modo: immediate"]:::immediate
    N2 --> N1
```

### Resumen de Tipos en la Expresión

- **string**: 2 ocurrencias
- **char**: 1 ocurrencias

---

# Fase 2: Síntesis
## 3. Representación Intermedia

### Notación Postfija (Polaca Inversa)
`nombre 'Hola Mundo' :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `:=`     | `nombre`     | `'Hola Mundo'`     |
