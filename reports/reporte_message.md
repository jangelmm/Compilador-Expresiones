# Reporte de Compilación para la Expresión

`message := 'Hola ' + 'Mundo'`

---

# Fase 1: Análisis
## 1.1. Análisis Lexicográfico

El código fuente se descompone en los siguientes tokens:

| Tipo | Valor | ID |
|------|-------|----|
| IDENTIFIER | `message` | 10723 |
| OPERATOR | `:=` | 101 |
| STRING | `'Hola '` | None |
| OPERATOR | `+` | 102 |
| STRING | `'Mundo'` | None |

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
| 10723 | message | string | 0 | 1000 | direct |

**Total de símbolos:** 1
**Siguiente dirección disponible:** 1004

---

## Fase 1.2: Análisis Sintáctico
### 1.2.1. Generación de Árbol de Expresión

La expresión se ha validado y convertido en un Árbol de Sintaxis Abstracta (AST), que representa su estructura operativa.

**Notación Postfija intermedia:** `message 'Hola ' 'Mundo' + :=`

```mermaid
graph TD
    N4((':='))
    N0(['message'])
    N4 --> N0
    N3(('+'))
    N1([''Hola ''])
    N3 --> N1
    N2([''Mundo''])
    N3 --> N2
    N4 --> N3
```

---
### 1.2.2. Comprobación Sintáctica / Comprobación de Tipos

La secuencia de tokens es válida según la gramática. Se genera el siguiente árbol de derivación:

```mermaid
graph TD
    n0['S'] --- n1['ID']
    n0['S'] --- n3[':=']
    n0['S'] --- n7['F']
    n1['ID'] --- n2['message']
    n7['F'] --- n4['I']
    n7['F'] --- n8['+']
    n7['F'] --- n9['I']
    n4['I'] --- n5['STRING']
    n9['I'] --- n10['STRING']
    n5['STRING'] --- n6[''Hola '']
    n10['STRING'] --- n11[''Mundo'']
```

---
## 1.3. Análisis Semántico

### Errores Semánticos Encontrados

- ERROR: Operación ':=' no permitida entre string y ERROR: Operación '+' no permitida entre char y char
- ERROR: Operación '+' no permitida entre char y char

Se verifica la compatibilidad de tipos recorriendo el AST. Cada nodo se anota con su tipo inferido o con un error.

```mermaid
graph TD
    classDef error fill:#ffdddd,stroke:#d44,stroke-width:2px;
    classDef default fill:#ddffdd,stroke:#4d4,stroke-width:2px;
    classDef immediate fill:#ddddff,stroke:#44d,stroke-width:2px;
    N4["<b>:=</b><br/><i>ERROR: Operación ':=' no permitida entre string y ERROR: Operación '+' no permitida entre char y char</i><br/>Modo: direct"]:::error
    N0["<b>message</b><br/><i>string</i><br/>Modo: direct<br/>Addr: 1000"]:::default
    N4 --> N0
    N3["<b>+</b><br/><i>ERROR: Operación '+' no permitida entre char y char</i><br/>Modo: register"]:::error
    N1["<b>'Hola '</b><br/><i>char</i><br/>Modo: immediate"]:::immediate
    N3 --> N1
    N2["<b>'Mundo'</b><br/><i>char</i><br/>Modo: immediate"]:::immediate
    N3 --> N2
    N4 --> N3
```

### Resumen de Tipos en la Expresión

- **string**: 1 ocurrencias
- **char**: 2 ocurrencias

---

# Fase 2: Síntesis
## 3. Representación Intermedia

### Notación Postfija (Polaca Inversa)
`message 'Hola ' 'Mundo' + :=`

### Tripletas
La expresión se traduce en la siguiente secuencia de instrucciones de tres direcciones:

| # | Operador | Operando 1 | Operando 2 |
|---|----------|------------|------------|
|(0)| `+`     | `'Hola '`     | `'Mundo'`     |
|(1)| `:=`     | `message`     | `(0)`     |
