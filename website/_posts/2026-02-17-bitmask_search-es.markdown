---
layout: post
title: "Busqueda con mascaras de bits"
date: 2026-02-17 22:18:19 -0300
lang: es
resource-programming-algorithm: true
permalink: /resource/bitmask_search.html
---

"Es una tecnica donde los subconjuntos de un conjunto finito se codifican como bits en un entero y se iteran exhaustivamente para explorar todas las combinaciones posibles."

> Traducción de <a {% static_href %}href="/resource/bitmask_search.html"{% endstatic_href %}>la publicación original en inglés</a>.

# Que es una mascara de bits y la busqueda con mascaras de bits?

Es una tecnica donde un conjunto de elecciones o estados se representa
como [bits](https://en.wikipedia.org/wiki/Bit) (0 o 1). La busqueda con
mascaras de bits consiste en iterar sobre esas representaciones para
explorar todas las combinaciones posibles.

En resumen, es una forma de representacion
([mask](https://en.wikipedia.org/wiki/Mask_(computing))) e iteracion
que hace que la fuerza bruta sea viable y mas simple para
[espacios discretos](https://en.wikipedia.org/wiki/Discrete_space)
pequenos.

## Por ejemplo: tenemos 4 elementos

-   Usamos un numero de 4 bits:
    -   `0000` -> no selecciona nada
    -   `0001` -> selecciona el elemento 0
    -   `1010` -> selecciona los elementos 1 y 3
    -   `1111` -> selecciona todos los elementos

Al iterar desde `0` hasta `(1<<n)-1`, enumeramos todos los subconjuntos
de `n` elementos.

## Importancia de esta tecnica

-   Es extremadamente compacta y rapida, porque se modela facilmente con
    operaciones bit a bit.
-   No hace falta usar arreglos ni recursion.

## Advertencias

Esta tecnica es exponencial (orden `2^n`); por lo tanto, la mejor forma
de volverla mas practica es *reducir constantes*.

# Implementacion

## 1. Representar un conjunto con una mascara

Con `n` elementos indexados de `0...n-1`, el bit `i` indica si el
elemento `i` pertenece al conjunto.

-   Probar si `i` esta en el conjunto: `(mask >> i) & 1`
-   Agregar el elemento `i`: `mask | (1<<i)`
-   Quitar el elemento `i`: `mask & ~(1<<i)`
-   Alternar el elemento `i`: `mask ^ (1<<i)`

*Nota: usar tipos sin signo para evitar problemas con bits de signo.*

## 2. Enumerar todos los subconjuntos

Este es el enfoque de fuerza bruta.

    for mask in [0 .. (1<<n)-1]:
        // mask is one subset
        evaluate(mask)

La funcion `evaluate` itera sobre todos los elementos contenidos en
`mask`.

Por ejemplo, iterando solo los bits encendidos:

    x = mask
    while x != 0:
        lsb = x & -x          // lowest set bit
        i = index_of(lsb)     // e.g., trailing_zeros(lsb)
        use(i)
        x -= lsb

La mayoria de los lenguajes ofrecen operaciones para contar ceros
finales (ctz):

-   C/C++: `__builtin_ctz`
-   Rust: `trailing_zeros()`
-   Python: `(lsb.bit_length() - 1)`

## 3. Enumerar submascaras

Dada una mascara, esto genera todas sus submascaras.

    sub = mask
    while True:
        use(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask

Esto genera todas las submascaras en orden descendente y es uno de los
patrones mas convenientes con mascaras de bits.

