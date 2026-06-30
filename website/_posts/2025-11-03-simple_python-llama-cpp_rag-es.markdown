---
layout: post
title: "Simple Llama.cpp RAG"
date: 2025-11-03 16:14:00 -0300
lang: es
resource-python: true
permalink: /resource/simple_python-llama-cpp_rag.html
---

Implementación simple de RAG usando `python-llama-cpp`.

> Traducción de <a {% static_href %}href="/resource/simple_python-llama-cpp_rag.html"{% endstatic_href %}>la publicación original en inglés</a>.

**DISCLAIMER:** hice este proyecto para uso *personal* y con fines de
*aprendizaje*, enfocado en entender RAG básico, modelos de embeddings y
ejecución local de IA. Por eso usé código generado por LLM para este
proyecto específico: escribir el código no era el objetivo principal.
Por la misma razón tiene bastantes asperezas, pero funciona. Como no
encontré una forma actualizada y directa de hacerlo en otro lado,
decidí publicarlo porque puede ser útil para alguien más.

- **Github link:** [GCaggianese/simple_python-llama-cpp_RAG](https://github.com/GCaggianese/simple_python-llama-cpp_RAG)
- **Codeberg link:** [GCaggianese/simple_python-llama-cpp_RAG](https://codeberg.org/GCaggianese/simple_python-llama-cpp_RAG)

# Prerrequisitos

## Requisitos del sistema

- Python 3.8+
- Compilador C (GCC, Clang, etc.)
- Ninja

## Instalar `requirements.txt`

```bash
pip install -r requirements.txt
```

## Soporte CUDA de Nvidia

La forma más simple de instalar `python-llama-cpp` con soporte CUDA
*(12.4)* es:

```bash
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 \
  --force-reinstall --no-cache-dir
```

Como se explica en [Github:
llama-cpp-python](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#installation-configuration).

`--force-reinstall --no-cache-dir` es importante; sin eso es probable
que reinstale desde cache sin soporte CUDA.

Este paso debería hacerse **después** de instalar `requirements.txt`.

### GNU Guix

Si usás GNU Guix, necesitás el canal `Nonguix` y también
[guix-hpc-non-free](https://gitlab.inria.fr/guix-hpc/guix-hpc-non-free).
Con esos canales, `nvidia-service-type` y `cuda-toolkit@12.4.0`, se
puede correr en GPU.

## Directorio docs

Crear un directorio `docs` para los documentos que querés que la IA use
como contexto.

```bash
mkdir docs
```

# Uso

Nota: si usás envrc, va a crear un directorio `venv` y activar el
entorno Python. Recomiendo usar ese `.envrc` sólo con GNU Guix, porque
agrega variables de entorno específicas para que funcione ahí.

1. Instalar todos los requirements de Python.
2. Ejecutar `python rag.py`.
   - Descarga los modelos (`granite-3.3-2b-instruct`,
     `all-MiniLM-L6-v2`).
   - Los carga en CPU/GPU.
   - Muestra el prompt interactivo.
   - **IMPORTANTE:** puede fallar en tu hardware; uso `n_ctx=8196` con
     4000 tokens, que puede ser demasiado para algunas máquinas.
3. Preguntar.

# Ejemplo

Probado con GNU Guix, Linux 6.16.12, Intel i7-11800H y NVIDIA RTX 3060
Ti.

Para probarlo con la página de Wikipedia de
[Simple Linear Regression](https://en.wikipedia.org/wiki/Simple_linear_regression):

1. Instalar `pandoc` y `wget`.
2. Descargar la página y convertirla a texto:

```bash
wget https://en.wikipedia.org/wiki/Simple_linear_regression
pandoc -f html -i Simple_linear_regression -o slr.txt
mv slr.txt docs
rm Simple_Linear_Regression
```

3. Ejecutar:

```bash
python rag.py
```

El modelo queda cargado y esperando preguntas. El ejemplo original
pregunta qué método se usa comúnmente en SLR y responde Ordinary Least
Squares usando contexto recuperado del documento.

