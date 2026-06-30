---
layout: post
title: "在 Termux 上執行 Jupyter Lab"
date: 2025-09-30 11:00:00 +0300
categories: zh_TW resource python
lang: zh_TW
resource-python: true
permalink: /resource/jupyter_Lab_on_Termux.html
---

這是一份在 Android 上執行 Jupyter Lab 的簡明指南。

> 本文翻譯自<a {% static_href %}href="/resource/jupyter_Lab_on_Termux.html"{% endstatic_href %}>英文原文</a>。

1.  更新 Termux

    ```sh
    apt update -y && apt upgrade -y
    ```

2.  安裝 Python、Clang、Rust 和 Binutils

    ```sh
    pkg i clang rust python3 binutils -y
    ```

3.  為 Jupyter 建立 `venv`

    ```sh
    python3 -n venv jupyter
    ```

    然後啟用它：

    ```sh
    source jupyter/bin/activate
    ```

    注意：我很確定也可以把它安裝到系統層級，因為 Termux 允許
    直接 `pip install` 東西，不過一般來說這不是好主意。

4.  更新 pip 並安裝需要的套件

    ```sh
    pip install --upgrade pip
    ```
    ```sh
    pip install wheel cython
    ```

5.  安裝 ZeroMQ 和 PyZMQ

    ```sh
    apt install libzmq -y
    ```
    ```sh
    pip install pyzmq
    ```

6.  最後：安裝 Jupyter

    ```sh
    pip install jupyter
    ```

現在就可以開始使用了。

