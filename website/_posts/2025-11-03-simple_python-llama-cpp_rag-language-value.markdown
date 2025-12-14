---
layout: post
title: "Simple Llama.cpp RAG"
date: 2025-11-03 16:14:00 -0300
lang: en
resource-python: true
permalink: /resource/simple_python-llama-cpp_rag.html
---

Simple RAG implementation using python-llama-cpp

**DISCLAIMER:** I did this project just for *personal* use and
*learning* purposes, focusing on understanding basic RAG, embedding
models, and running local AI. Therefore, I used LLM-generated code for
this specific project, as the coding itself was not the objective. For
the same reason, it has a lot of rough edges, but it works. Since I
didn't find an updated, straightforward way to do this anywhere else, I
decided to post it, as I felt it might be useful to someone else.

- **Github link:** [GCaggianese/simple_python-llama-cpp_RAG](https://github.com/GCaggianese/simple_python-llama-cpp_RAG)
- **Codeberg link:** [GCaggianese/simple_python-llama-cpp_RAG](https://codeberg.org/GCaggianese/simple_python-llama-cpp_RAG)

# Pre-requisites:

## System Requirements:

-   Python 3.8+
-   C Compiler (GCC, Clang, etc.)
-   Ninja

## Install Python `requirements.txt`

``` bash
pip install -r requirements.txt
```

## For Nvidia CUDA support:

-   The easiest way to install `python-llama-cpp` with CUDA *(12.4)*
    support is using

    ``` bash
    CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python \
      --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 \
      --force-reinstall --no-cache-dir
    ```

    As explained in [Github:
    llama-cpp-python](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#installation-configuration).

    -   Notice the `--force-reinstall --no-cache-dir`, those are
        mandatory as if not it will likely reinstall from cache without
        CUDA support.

-   This step should be done AFTER installing the `requirements.txt`.

### GNU Guix

If you're using GNU Guix you'll need not only the `Nonguix` channel but
also
[guix-hpc-non-free](https://gitlab.inria.fr/guix-hpc/guix-hpc-non-free).
Whith those channels, having the `nvidia-service-type` and the
`cuda-toolkit@12.4.0`, you'll be able to run it on the GPU.

## Docs directory

Create a `docs` directory for the documents, you'll put here the stuff
you want the AI to retrieve context from.

``` bash
mkdir docs
```

# Usage:

Note: if you use envrc it will create a `venv` directory and activate a
Python it's venv. I suggest only using this .envrc only if you're using
GNU Guix as it adds some environment variables to make it work there.

1.  Install all the Python requirements.
2.  Run `python rag.py`
    -   It will now download the models (granite-3.3-2b-instruct,
        all-MiniLM-L6-v2).
    -   Then those will be loaded on your CPU/GPU.
    -   You'll see the interactive prompt.
    -   **IMPORTANT:** It may fail on your hardware as I'm using a
        `n_ctx=8196` with 4000 tokens, that may be way too much for some
        hardware (not to mention the model itself is not that small).
3.  Ask!

# Examples:

Tested with:

-   OS: GNU Guix
-   Kernel: Linux 6.16.12
-   CPU: 11th Gen Intel(R) Core(TM) i7-11800H (16) @ 4.60 GHz
-   GPU: NVIDIA GeForce RTX 3060 Ti Driver Version: 580.82.09 CUDA
    Version: 13.0 CUDA ToolKit Version: 12.4.0

## Asking questions about [Simple Linear Regression (SLR)](https://en.wikipedia.org/wiki/Simple_linear_regression) from Wikipedia

1.  Install `pandoc` and `wget` This is only needed for downloading the
    webpage into a txt and **not needed** for the RAG itself, if you
    already have a .txt or a .pdf just go ahead and use those ;)

2.  Download the page and convert it into a .txt (this is not actually
    needed but will clean the document and help the model to find
    meaningful context).

    ``` bash
    wget https://en.wikipedia.org/wiki/Simple_linear_regression
    pandoc -f html -i Simple_linear_regression -o slr.txt
    mv slr.txt docs
    rm Simple_Linear_Regression
    ```

3.  Run: `python rag.py`

**Output:**

    ❯ python rag.py
    llama_context: n_ctx_per_seq (8196) < n_ctx_train (131072) -- the full capacity of the model will not be utilized
    Interactive mode – type '/bye' or Ctrl-D to quit.

    🤖 >

-   The model is loaded and waiting for questions.

**Ask!**

    🤖 > which method is common stipulated to be used in SLR?
    Question: which method is common stipulated to be used in SLR?
    Answer:  The common and stipulated method used in Simple Linear Regression (SLR) is the Ordinary Least Squares (OLS) method.
    This method estimates the coefficients of the linear equation that best fits the data according to a defined criterion, which in this case is minimizing the sum of squared residuals (the differences between observed values and values predicted by the model).
    Time taken: 1.24 seconds

    Context used:

    Doc 1: In statistics, simple linear regression (SLR) is a linear regression model with a single explanatory variable. That is, it concerns two-dimensional sample points with one independent variable and one ...

    Doc 2: In statistics, simple linear regression (SLR) is a linear regression model with a single explanatory variable. That is, it concerns two-dimensional sample points with one independent variable and one ...
