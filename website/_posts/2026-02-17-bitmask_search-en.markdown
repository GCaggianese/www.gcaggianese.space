---
layout: post
title: "Bitmask Search"
date: 2026-02-17 22:18:19 -0300
lang: en
resource-programming-algorithm: true
permalink: /resource/bitmask_search.html
---

"Is a technique where subsets of a finite set are encoded as bits in an integer and exhaustively iterated to explore all possible combinations."

# What is Bitmask and Bitmask Search?

It is a technique where a set of choices or states is represented as
[bits](https://en.wikipedia.org/wiki/Bit) (0 or 1). Bitmask search
consists of iterating over those representations to explore all possible
combinations.

In short, it is a way of representation
([mask](https://en.wikipedia.org/wiki/Mask_(computing))) and iteration
that makes brute force feasible and easier for small [discrete
spaces](https://en.wikipedia.org/wiki/Discrete_space).

## For example: we have 4 items

-   We use a 4-bit number:
    -   `0000` → selects nothing
    -   `0001` → selects item 0
    -   `1010` → selects items 1 and 3
    -   `1111` → selects all items

By iterating from `0` to `(1<<n)-1`, we enumerate all subsets of `n`
elements.

## Importance of this technique

-   It is extremely compact and fast, as it is easily modeled with
    bitwise operations
-   No need for arrays or recursion

## Caveats

This technique is exponential (order `2^n`); therefore, the best way to
improve its practicality is by *reducing constants*.

# Implementation

## 1. Representing a set with a mask

Having `n` items indexed `0…n-1`, bit `i` indicates whether item `i` is
in the set.

-   Test if `i` is in the set: `(mask >> i) & 1`
-   Add item `i`: `mask | (1<<i)`
-   Remove item `i`: `mask & ~(1<<i)`
-   Toggle item `i`: `mask ^ (1<<i)`

*Note: use unsigned types to avoid issues with sign bits.*

## 2. Enumerate all subsets

This is the brute-force approach.

    for mask in [0 .. (1<<n)-1]:
        // mask is one subset
        evaluate(mask)

The `evaluate` function iterates over all elements contained in `mask`.

For example, iterating only the set bits:

    x = mask
    while x != 0:
        lsb = x & -x          // lowest set bit
        i = index_of(lsb)     // e.g., trailing_zeros(lsb)
        use(i)
        x -= lsb

Most languages provide trailing-zeros (ctz) operations:

-   C/C++: `__builtin_ctz`
-   Rust: `trailing_zeros()`
-   Python: `(lsb.bit_length() - 1)`

## 3. Enumerate submasks

Given a mask, this generates all of its submasks.

    sub = mask
    while True:
        use(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask

This generates all submasks in descending order and is one of the most
convenient bitmask patterns.
