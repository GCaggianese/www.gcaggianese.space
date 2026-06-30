---
layout: post
title: "位元遮罩搜尋"
date: 2026-02-17 22:18:19 -0300
lang: zh_TW
resource-programming-algorithm: true
permalink: /resource/bitmask_search.html
---

「這是一種技術：把有限集合的子集合編碼成整數中的位元，然後窮舉迭代，以探索所有可能的組合。」

> 本文翻譯自<a {% static_href %}href="/resource/bitmask_search.html"{% endstatic_href %}>英文原文</a>。

# 什麼是位元遮罩與位元遮罩搜尋？

這是一種用 [bits](https://en.wikipedia.org/wiki/Bit)（0 或 1）表示
一組選擇或狀態的技術。位元遮罩搜尋則是迭代這些表示法，以探索所有
可能的組合。

簡而言之，這是一種表示
（[mask](https://en.wikipedia.org/wiki/Mask_(computing))）和迭代方式，
讓小型[離散空間](https://en.wikipedia.org/wiki/Discrete_space)中的暴力搜尋
變得可行且更容易處理。

## 例如：有 4 個項目

-   我們使用一個 4 位元數字：
    -   `0000` -> 什麼都不選
    -   `0001` -> 選擇項目 0
    -   `1010` -> 選擇項目 1 和 3
    -   `1111` -> 選擇所有項目

從 `0` 迭代到 `(1<<n)-1`，就能枚舉 `n` 個元素的所有子集合。

## 這項技術的重要性

-   它非常緊湊且快速，因為很容易用位元運算建模。
-   不需要陣列或遞迴。

## 注意事項

這項技術是指數級的（階數 `2^n`）；因此，要提升實用性，最好的方式是
*降低常數*。

# 實作

## 1. 用遮罩表示集合

有 `n` 個項目，索引為 `0...n-1`，第 `i` 個位元表示項目 `i`
是否在集合中。

-   測試 `i` 是否在集合中：`(mask >> i) & 1`
-   加入項目 `i`：`mask | (1<<i)`
-   移除項目 `i`：`mask & ~(1<<i)`
-   切換項目 `i`：`mask ^ (1<<i)`

*注意：使用無號型別，以避免符號位元造成問題。*

## 2. 枚舉所有子集合

這是暴力搜尋的方法。

    for mask in [0 .. (1<<n)-1]:
        // mask is one subset
        evaluate(mask)

`evaluate` 函式會迭代 `mask` 中包含的所有元素。

例如，只迭代已設定的位元：

    x = mask
    while x != 0:
        lsb = x & -x          // lowest set bit
        i = index_of(lsb)     // e.g., trailing_zeros(lsb)
        use(i)
        x -= lsb

多數語言都提供 trailing-zeros（ctz）操作：

-   C/C++：`__builtin_ctz`
-   Rust：`trailing_zeros()`
-   Python：`(lsb.bit_length() - 1)`

## 3. 枚舉子遮罩

給定一個遮罩，這會產生它的所有子遮罩。

    sub = mask
    while True:
        use(sub)
        if sub == 0:
            break
        sub = (sub - 1) & mask

這會以遞減順序產生所有子遮罩，也是位元遮罩中最方便的模式之一。

