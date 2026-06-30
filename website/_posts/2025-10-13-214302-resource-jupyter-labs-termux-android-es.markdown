---
layout: post
title: "Jupyter Lab en Termux"
date: 2025-09-30 11:00:00 +0300
categories: es resource python
lang: es
resource-python: true
permalink: /resource/jupyter_Lab_on_Termux.html
---

Una guía directa para ejecutar Jupyter Lab en Android.

> Traducción de <a {% static_href %}href="/resource/jupyter_Lab_on_Termux.html"{% endstatic_href %}>la publicación original en inglés</a>.

1.  Actualizar Termux

    ```sh
    apt update -y && apt upgrade -y
    ```

2.  Instalar Python, Clang, Rust y Binutils

    ```sh
    pkg i clang rust python3 binutils -y
    ```

3.  Crear un `venv` para Jupyter

    ```sh
    python3 -n venv jupyter
    ```

    Y después activarlo:

    ```sh
    source jupyter/bin/activate
    ```

    Nota: estoy bastante seguro de que se puede instalar a nivel de
    sistema, porque Termux permite hacer `pip install` directamente,
    aunque en general no es una buena idea.

4.  Actualizar pip e instalar los paquetes necesarios

    ```sh
    pip install --upgrade pip
    ```
    ```sh
    pip install wheel cython
    ```

5.  Instalar ZeroMQ y PyZMQ

    ```sh
    apt install libzmq -y
    ```
    ```sh
    pip install pyzmq
    ```

6.  Finalmente: instalar Jupyter

    ```sh
    pip install jupyter
    ```

Con eso ya queda listo.

