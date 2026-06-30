---
layout: post
title: "Simple Llama.cpp RAG"
date: 2025-11-03 16:14:00 -0300
lang: zh_TW
resource-python: true
permalink: /resource/simple_python-llama-cpp_rag.html
---

使用 `python-llama-cpp` 的簡單 RAG 實作。

> 本文翻譯自<a {% static_href %}href="/resource/simple_python-llama-cpp_rag.html"{% endstatic_href %}>英文原文</a>。

**DISCLAIMER:** 這個專案是為了*個人使用*和*學習目的*而做，重點是理解
基本 RAG、embedding models，以及在本機執行 AI。因此，這個特定專案使用了
LLM 產生的程式碼，因為寫程式本身不是主要目標。也因此它有不少粗糙的地方，
但可以運作。因為我沒有找到更新且直接的做法，所以決定把它貼出來，希望對
其他人有用。

- **Github link:** [GCaggianese/simple_python-llama-cpp_RAG](https://github.com/GCaggianese/simple_python-llama-cpp_RAG)
- **Codeberg link:** [GCaggianese/simple_python-llama-cpp_RAG](https://codeberg.org/GCaggianese/simple_python-llama-cpp_RAG)

# 前置需求

## 系統需求

- Python 3.8+
- C compiler（GCC、Clang 等）
- Ninja

## 安裝 Python `requirements.txt`

```bash
pip install -r requirements.txt
```

## Nvidia CUDA 支援

安裝支援 CUDA *(12.4)* 的 `python-llama-cpp` 最簡單方式是：

```bash
CMAKE_ARGS="-DGGML_CUDA=on" pip install llama-cpp-python \
  --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu124 \
  --force-reinstall --no-cache-dir
```

如 [Github:
llama-cpp-python](https://github.com/abetlen/llama-cpp-python?tab=readme-ov-file#installation-configuration)
所述，`--force-reinstall --no-cache-dir` 很重要，否則可能從 cache
重新安裝而沒有 CUDA 支援。

這個步驟應該在安裝 `requirements.txt` **之後**進行。

### GNU Guix

如果使用 GNU Guix，需要 `Nonguix` channel，也需要
[guix-hpc-non-free](https://gitlab.inria.fr/guix-hpc/guix-hpc-non-free)。
有這些 channels、`nvidia-service-type` 和 `cuda-toolkit@12.4.0` 後，
就能在 GPU 上執行。

## docs 目錄

建立 `docs` 目錄，把想讓 AI 從中取回上下文的文件放在這裡。

```bash
mkdir docs
```

# 使用

如果使用 envrc，它會建立 `venv` 目錄並啟用 Python venv。我建議只有在
GNU Guix 中才使用這個 `.envrc`，因為它會加入一些讓 Guix 環境可運作的
環境變數。

1. 安裝所有 Python requirements。
2. 執行 `python rag.py`。
   - 它會下載模型（`granite-3.3-2b-instruct`、`all-MiniLM-L6-v2`）。
   - 然後載入到 CPU/GPU。
   - 你會看到互動式 prompt。
   - **重要：** 它可能在你的硬體上失敗；我使用 `n_ctx=8196` 和 4000
     tokens，對某些硬體可能太大。
3. 開始提問。

# 範例

原文在 GNU Guix、Linux 6.16.12、Intel i7-11800H 與 NVIDIA RTX 3060 Ti
上測試。

用 Wikipedia 的
[Simple Linear Regression](https://en.wikipedia.org/wiki/Simple_linear_regression)
頁面測試：

```bash
wget https://en.wikipedia.org/wiki/Simple_linear_regression
pandoc -f html -i Simple_linear_regression -o slr.txt
mv slr.txt docs
rm Simple_Linear_Regression
python rag.py
```

模型會載入並等待問題。原始範例詢問 SLR 常用的方法，模型根據取回的文件
上下文回答 Ordinary Least Squares。

