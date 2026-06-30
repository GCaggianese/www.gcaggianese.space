---
layout: post
title: "llmrex"
date: 2026-05-13 17:58:00 -0300
lang: zh_TW
project: true
permalink: /project/llmrex.html
---

使用 GNU Screen IPC 與本機 1B LLM inference，在 CPU-only hardware 上即時控制終端機遊戲的 agent。

> 本文翻譯自<a {% static_href %}href="/project/llmrex.html"{% endstatic_href %}>英文原文</a>。

# llmrex

> 一個本機 1B LLM 透過 GNU Screen IPC 即時玩終端機 dinosaur game。CPU-only。不需要 GPU。

![demo](../assets/demo.gif)

**Github:** [GCaggianese/llmrex](https://github.com/GCaggianese/llmrex)

## 這是什麼

一個小型 framework，用來把本機 LLM 接到終端機遊戲中，作為 live agents。

第一個目標是 [SATYADAHAL/termrex](https://github.com/SATYADAHAL/termrex) 的 fork，也就是 Chrome dinosaur game 的 C++ 終端機版本。Controller 與 parser 用 [D](https://dlang.org/) 寫成。GNU Screen 提供 IPC backbone，同時暴露 keystroke injection 與 live terminal-content capture。

模型可以透過 Ollama 在本機執行（推薦），也可以透過 Gemini 2.5 Flash 這類 hosted backend 執行。

## 為什麼存在這個專案

大多數「LLM agents」都在高延遲、推論預算很大的環境中運作。

這個專案探索相反的限制：

- 緊湊的 real-time loops
- CPU-only local inference
- 最小 symbolic state extraction
- deterministic action serialization
- 系統之間的低延遲 IPC

有趣的問題不是 dinosaur game 本身，而是圍繞一個非常小的本機模型，建立可靠的 realtime agent loop。

## 這個系統解決的三個問題

1. 從正在執行的終端機應用程式擷取 live game state
2. 即時把 actions 注入回遊戲
3. 讓完整 inference loop 維持在實用的 latency budget 內

## 架構

![mermaid](../assets/llmrex_mermaid.png)

## 運作方式

### GNU Screen 作為 IPC backbone

命名的 GNU Screen sessions 剛好提供所需的兩個 primitives：

* `screen -X stuff " "` 將 keystroke 注入 session
* `screen -X hardcopy <file>` 將目前可見的 terminal content dump 到檔案

這建立了一個完整的雙向 channel：

* 讀出 state
* 把 input 推回去

不需要 custom IPC layer，遊戲本身也不需要暴露任何 internal state。

使用 Screen 作為 transport layer，是讓這個專案能以最小複雜度變得實用的關鍵架構決策。

### 放慢遊戲

社群的 dinosaur game 終端機 ports 對實用的 CPU-only local inference 來說跑得太快。

修正方式是修改 termrex 的 internal timing 與 physics step rate。Input handling 部分綁在 frame-refresh loop 上，所以放慢遊戲也破壞了 keypress responsiveness。Input loop 必須被解耦，並且部分重寫。

Flying enemies 透過 runtime flag 停用：

```bash
--no-obstacle-dino
```

這刻意把 action space 限制成單一 binary decision：

* jump
* wait

目標是展示穩定的 real-time inference loop，而不是最大化 gameplay complexity。

### Parser：從 ASCII art 到 symbolic state

`parser.d` 從 live terminal snapshot 中抽取單一 distance signal：

1. 找到 game frame 的底部邊界（`╰`）
2. 讀取 playfield row
3. 搜尋 cactus signatures（`||_`、`| |`）
4. 計算 dinosaur 到最近 obstacle 的距離

輸出很簡單：

* 以 characters 表示的距離
* 或在沒有可見物件時輸出 `-1`

模型永遠不會直接看到 ASCII rendering。

不需要 image processing 或 spatial reasoning。

### 為什麼用本機 LLM

Hosted APIs 不適合緊湊的 real-time loops：

* rate limits
* network latency
* response times 長
* inference delays 不可預測

單一 hosted response 可能比多個遊戲 obstacles 還久。

Local inference 完全移除這些限制，但引入另一個限制：

模型必須非常小且快速。

目標硬體是：

* Intel 11th-gen i7
* 32GB DDR4
* no GPU

## Model testing results

透過 Ollama 測試了幾個 models。

### IBM Granite 4 (1B quantized)

最佳實用結果。

* 快到足以 real-time play
* JSON formatting 可靠
* 在重複 loops 下 behavior 穩定

### Qwen reasoning variants

推理能力更強，但不適合 real time。

模型經常進入延長的 reasoning sequences，把簡單 actions 變成數分鐘的 pauses。

### 更小的 sub-1B models

產生一致、可 parse 的 output 時太不可靠。

### Hosted backend：Gemini 2.5 Flash

主要為實驗與比較而支援。

Hosted path 透過 actions 之間的強制 delay 來遵守 API limits。

## "logic gate" prompt

最初設計是把 raw ASCII frames 直接傳給模型。

小型本機 models 對空間 layout 的解讀表現很差。

解法是把大部分 decision-making 移到 deterministic preprocessing。

Parser 將 obstacle distance 轉成 symbolic sensor states：

* `URGENT`
* `WARNING`
* `SAFE`

接著模型被明確設定成 deterministic logic gate：

```text
System: You are a machine logic gate. Output ONLY JSON.
Rule 1: If SENSOR is URGENT, you must output the JUMP JSON.
Rule 2: If SENSOR is SAFE or WARNING, you must output the WAIT JSON.

Input MAP:    YOU-DISTANCE-15-D-DEAD
Input SENSOR: URGENT

JUMP JSON: {"dinosaur_game": "jump", "args": true}
WAIT JSON: {"dinosaur_game": "wait", "args": false}

Output:
```

這刻意用可靠性換掉模型的「智慧」。

大部分 reasoning 發生在 parser layer；模型的工作變成在嚴格 latency constraints 下穩定地序列化 action。

這個 trade-off 讓本機 1B model 能在 CPU-only hardware 上運行於 real-time loop 中。

## 執行

### Dependencies

* Linux
* [GNU Screen](https://www.gnu.org/software/screen/)
* D compiler（`dmd`、`ldc2` 或 `gdc`）
* [Ollama](https://ollama.com/)

Optional：

* `GEMINI_API_KEY` 用於 hosted inference

## Setup

```bash
# 1. Pull the local model
ollama pull granite4:1b

# 2. Clone this repository
git clone <REPO_URL>
cd llmrex

# 3. Build the patched termrex
cd termrex
make

# 4. Build the agent
cd ..
mkdir -p build
dmd -of=build/agent agent.d parser.d -L-lcurl
```

## Play

### Terminal A — start the game

```bash
screen -S dino
./termrex/build/termrex \
    --ascii-only \
    --no-obstacle-dino \
    --skip-intro
```

### Terminal B — run the agent

不要忘記啟用 ollama
``` bash
ollama serve &
```

```bash
./build/agent \
    --ollama \
    --model granite4:1b \
    --urgent 35 # adjust the offset to match the inference delay of your setup
```

## CLI flags

* `--ollama`
  使用本機 Ollama backend

* `--model <name>`
  Ollama model tag（default：`granite4:1b`）

* `--urgent <n>`
  觸發 jump 的 character distance threshold

* `--dir <path>`
  用於 snapshot generation 的 project root path

## Gemini backend

匯出 Gemini API key 並省略 `--ollama`：

```bash
export GEMINI_API_KEY=...
```

## 限制與未來工作

### 手動調整的 timing

目前的 game speed 是針對測試硬體與模型手動校準。

更好的系統會：

* 在 startup benchmark tokens/sec
* 動態調整 game speed
* 自動調整 inference pacing

### Stateless prompts

模型在 frames 之間沒有 memory。

有限的 short-term context 可能改善 prediction 與 timing consistency。

### Single-action gameplay

Flying enemies 被停用，以保持 action space 為 binary。

支援它們需要：

* parser height detection
* additional sensor channels
* 第二個 action（`duck`）

### Parser-heavy architecture

目前大部分 reasoning 發生在 inference 之前。

這是刻意的：它讓小模型能可靠地即時運作。

更強的本機 models 可以把部分 decision-making 移回 inference layer。

## Credits

* Upstream game：[SATYADAHAL/termrex](https://github.com/SATYADAHAL/termrex)
* Local inference：[Ollama](https://ollama.com/)
* Model：[IBM Granite](https://www.ibm.com/granite)
* Optional hosted backend：Gemini 2.5 Flash
