# Reporte de Compilación

```pascal

        program Prueba;
        var
          x, y : integer;
          flag : boolean;
        
        begin
          x := 10;
          y := 5;
          flag := (x > 5) and (y < 10);
        end.
        
```

---

# Fase 0: Análisis de Declaraciones

## Tabla de Símbolos Variables (Declaradas)

## Tabla de Símbolos Variables

| ID | Nombre | Tipo | Scope | Dirección |
|----|--------|------|-------|-----------|
| 10797 | x | integer | 0 | 1000 |
| 10365 | y | integer | 0 | 1004 |
| 10221 | flag | boolean | 0 | 1008 |

**Total de símbolos:** 3
**Siguiente dirección disponible:** 100C

---

# Fase 1: Análisis
## 1.1. Análisis Lexicográfico

El código fuente se descompone en los siguientes tokens:

| Token | Lexema | ID Tabla |
|-------|--------|----------|
| RESERVED_WORD | `program` | 8 |
| PROGRAM_NAME | `prueba` | PROGRAM |
| DELIMITER | `;` | 202 |
| RESERVED_WORD | `var` | 1 |
| IDENTIFIER | `x` | 10797 |
| COMMA | `,` | None |
| IDENTIFIER | `y` | 10365 |
| COLON | `:` | None |
| RESERVED_WORD | `integer` | 5 |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `flag` | 10221 |
| COLON | `:` | None |
| RESERVED_WORD | `boolean` | 9 |
| DELIMITER | `;` | 202 |
| RESERVED_WORD | `begin` | 3 |
| IDENTIFIER | `x` | 10797 |
| OPERATOR | `:=` | 101 |
| CONSTANT | `10` | None |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `y` | 10365 |
| OPERATOR | `:=` | 101 |
| CONSTANT | `5` | None |
| DELIMITER | `;` | 202 |
| IDENTIFIER | `flag` | 10221 |
| OPERATOR | `:=` | 101 |
| PAREN | `(` | None |
| IDENTIFIER | `x` | 10797 |
| OPERATOR | `>` | 108 |
| CONSTANT | `5` | None |
| PAREN | `)` | None |
| OPERATOR | `and` | 112 |
| PAREN | `(` | None |
| IDENTIFIER | `y` | 10365 |
| OPERATOR | `<` | 107 |
| CONSTANT | `10` | None |
| PAREN | `)` | None |
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

**Notación Postfija intermedia:** `x 10 :=`

```mermaid
graph TD
    N2((':='))
    N0(['x'])
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
    n1['ID'] --- n2['x']
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
    N0["<b>x</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1000"]:::default
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
`x 10 :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `:=`     | `x`     | `10`     |

### Sentencia 2
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `y 5 :=`

```mermaid
graph TD
    N2((':='))
    N0(['y'])
    N2 --> N0
    N1(['5'])
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
    n8['ID'] --- n9['y']
    n11['I'] --- n12['NUM']
    n12['NUM'] --- n13['5']
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
    N0["<b>y</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1004"]:::default
    N2 --> N0
    N1["<b>5</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N2 --> N1
```

### Resumen de Tipos en la Expresión

- **integer**: 3 ocurrencias

---

# Fase 2: Síntesis
## 3. Representación Intermedia

### Notación Postfija (Polaca Inversa)
`y 5 :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `:=`     | `y`     | `5`     |

### Sentencia 3
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `flag x 5 > y 10 < and :=`

```mermaid
graph TD
    N8((':='))
    N0(['flag'])
    N8 --> N0
    N7(('and'))
    N3(('>'))
    N1(['x'])
    N3 --> N1
    N2(['5'])
    N3 --> N2
    N7 --> N3
    N6(('<'))
    N4(['y'])
    N6 --> N4
    N5(['10'])
    N6 --> N5
    N7 --> N6
    N8 --> N7
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n14['S'] --- n15['ID']
    n14['S'] --- n17[':=']
    n14['S'] --- n27['E']
    n15['ID'] --- n16['flag']
    n27['E'] --- n18['I']
    n27['E'] --- n28['and']
    n27['E'] --- n29['I']
    n18['I'] --- n22['T']
    n29['I'] --- n33['T']
    n22['T'] --- n19['I']
    n22['T'] --- n23['>']
    n22['T'] --- n24['I']
    n33['T'] --- n30['I']
    n33['T'] --- n34['<']
    n33['T'] --- n35['I']
    n19['I'] --- n20['ID']
    n24['I'] --- n25['NUM']
    n30['I'] --- n31['ID']
    n35['I'] --- n36['NUM']
    n20['ID'] --- n21['x']
    n25['NUM'] --- n26['5']
    n31['ID'] --- n32['y']
    n36['NUM'] --- n37['10']
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
    N0["<b>flag</b><br/><i>boolean</i><br/>Modo: direct<br/>Addr: 1008"]:::default
    N8 --> N0
    N7["<b>and</b><br/><i>boolean</i><br/>Modo: register"]:::default
    N3["<b>></b><br/><i>boolean</i><br/>Modo: register"]:::default
    N1["<b>x</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1000"]:::default
    N3 --> N1
    N2["<b>5</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
    N3 --> N2
    N7 --> N3
    N6["<b><</b><br/><i>boolean</i><br/>Modo: register"]:::default
    N4["<b>y</b><br/><i>integer</i><br/>Modo: direct<br/>Addr: 1004"]:::default
    N6 --> N4
    N5["<b>10</b><br/><i>integer</i><br/>Modo: immediate"]:::immediate
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
`flag x 5 > y 10 < and :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `>`     | `x`     | `5`     |
|(1)| `<`     | `y`     | `10`     |
|(2)| `and`     | `(0)`     | `(1)`     |
|(3)| `:=`     | `flag`     | `(2)`     |
