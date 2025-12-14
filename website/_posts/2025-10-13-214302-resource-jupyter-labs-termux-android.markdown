---
layout: post
title: "Jupyter Lab on Termux"
date: 2025-09-30 11:00:00 +0300
categories: en resource python
lang: en
resource-python: true
permalink: /resource/jupyter_Lab_on_Termux.html
---

A straightforward guide to running Jupyter Lab on Android.

1.  Update and Upgrade Termux

    ```sh
    apt update -y && apt upgrade -y
    ```

2.  Install Python, Clang, Rust and Binutils

    ```sh
    pkg i clang rust python3 binutils -y
    ```

3.  Create a `venv` for Jupyter

    ```sh
    python3 -n venv jupyter
    ```

    And then activate it

    ```sh
    source jupyter/bin/activate
    ```

    Note: I'm pretty sure you might be able to install it system wide
    as termux let's you just `pip install` stuff, though in general it
    is not a good idea.

4.  Upgrade pip and Install Required Packages

    ```sh
    pip install --upgrade pip
    ```
    ```sh
    pip install wheel cython
    ```

5.  Install ZeroMQ and PyZMQ

    ```sh
    apt install libzmq -y
    ```
    ```sh
    pip install pyzmq
    ```

6.  Finally: Install Jupyter

    ```sh
    pip install jupyter
    ```

Now you're ready to go!
