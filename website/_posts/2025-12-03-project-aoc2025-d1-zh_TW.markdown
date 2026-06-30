---
layout: post
title: "Advent of Code 2025 - 第 1 天：C++"
date: 2025-12-03 20:46:39 -0300
lang: zh_TW
project-aoc2025: true
permalink: /project/aoc2025d1.html
---

「因為新的安全協定，密碼被鎖在下面的保險箱裡。請查看附件文件取得新的組合。」

> 本文翻譯自<a {% static_href %}href="/project/aoc2025d1.html"{% endstatic_href %}>英文原文</a>。

**Github**: *[GCaggianese/AoC-2025/D2](https://github.com/GCaggianese/AoC-2025/tree/master/D2)*
   - [Standard C++](https://isocpp.org/)

# 題目 [第 1 天 - Advent of Code](https://adventofcode.com/2025/day/1)

-   轉盤從 00 到 99（NN），到達每個數字時會發出一次 **click**。
    -   這表示共有 100 個可能值，之後會循環。

## 輸入結構

-   **旋轉**序列（每行一個）

    -   `L` -> 往較小的數字旋轉
    -   `R` -> 往較大的數字旋轉

-   使用 `%` 做循環；在 C++ 中使用
    [模運算（Gauss）](https://en.wikipedia.org/wiki/Modular_arithmetic)，
    並採用向下取整的除法慣例。

-   `NN` -> 旋轉次數。

-   起始位置是 50。

# 使用 C++ STD 20 的解法

-   Meson 只是因為我在 AoC 之前剛好在學它。也可以直接用
    `g++ src/main.cpp -o aoc-2020-d1`，或任何你喜歡的方式。
-   實際上我是用 `org-babbel` 解的。

- **Github link:** [GCaggianese/AoC-2025](https://github.com/GCaggianese/AoC-2025/tree/master/D1)
- **Codeberg link:** [GCaggianese/AoC-2025](https://codeberg.org/GCaggianese/AoC-2025/src/branch/master/D1)

```
    ...
    R31
    Dial position: 86
    R25
    Dial position: 11
    Clicks: 1129
```

正確答案~! 🌟+1

------------------------------------------------------------------------


    int dial = 50;
    int clicker = 0;

    template <typename T> T floor_mod(T a, T b) {
        return a - b * std::floor(static_cast<double>(a) / static_cast<double>(b));
    }

    void fright(int r) { dial = floor_mod((dial + r), 100); }

    void fleft(int l) { dial = floor_mod((dial - l), 100); }

    void click() {
        if (dial == 0) {
            clicker += 1;
        }
    }

    void parse_file(std::string_view filepath) {
        std::ifstream file(filepath.data());

        for (std::string line; std::getline(file, line);) {
            if (line.empty())
                continue;

            char direction = line[0];

            int value = 0;
            auto [ptr, ec] =
                std::from_chars(line.data() + 1, line.data() + line.size(), value);

            if (ec == std::errc{}) { // Success
                std::cout << line << '\n';

                if (direction == 'L') {
                    fleft(value);
                    click();
                    std::cout << "Dial position: " << dial << "\n";
                } else if (direction == 'R') {
                    fright(value);
                    click();
                    std::cout << "Dial position: " << dial << "\n";
                }
            }
            if (ec != std::errc{}) { // Fail
                std::cerr << "Parse error on line: " << line << '\n';
                continue;
            }
        }
    }

    int main(){

        std::cout << "Hey AoC 2025!\n\n";
        parse_file("input_test.txt");
        std::cout << "Clicks: " << clicker << "\n";

        return 0;
    }

