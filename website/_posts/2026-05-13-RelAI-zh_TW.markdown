---
layout: post
title: "RelAI"
date: 2026-05-13 22:21:43 -0300
lang: zh_TW
project: true
permalink: /project/relai.html
---

在瀏覽器中使用 OpenAI Realtime Translation、WebRTC、TypeScript、Vite，以及提供 ephemeral token 的 FastAPI backend，進行即時語音翻譯。

> 本文翻譯自<a {% static_href %}href="/project/relai.html"{% endstatic_href %}>英文原文</a>。

# RelAI

**Github:** [GCaggianese/RelAI](https://github.com/GCaggianese/RelAI)

RelAI 是一個以瀏覽器為基礎、用於即時語音翻譯的 MVP。

它使用 `getUserMedia` 擷取麥克風音訊，透過 WebRTC peer connection 將音訊送到 OpenAI，把翻譯後的語音作為 remote audio track 接收，並從 realtime data-channel events 顯示來源與翻譯後的逐字稿。

Backend 刻意保持很小：它只建立 ephemeral client secrets，因此長期有效的 OpenAI API key 永遠不需要暴露給瀏覽器。

## 狀態

可運作的 MVP。

已實作：

- 瀏覽器麥克風擷取
- 與 OpenAI Realtime Translation 建立 WebRTC session
- 翻譯音訊播放
- 來源逐字稿字幕
- 翻譯逐字稿字幕
- 用於 ephemeral client secrets 的 FastAPI backend
- 基本 session lifecycle 處理
- WebRTC connection-state logging
- Firefox/Zen 相容性警告

延後：

- 完整 interpreter mode
- 行動裝置 wrapper
- Production deployment
- 持久化 session history
- 進階 audio routing
- Authentication / user accounts

RelAI 還不是一個 polished product。它是一個可運作的 prototype，專注於端到端驗證即時語音翻譯 loop。

## 為什麼存在這個專案

大多數 AI 翻譯 demo 會把有趣的部分藏在一般 request/response API 後面。

RelAI 探索的是較低層的路徑：

- live microphone streaming
- WebRTC offer/answer exchange
- browser media permissions
- remote translated audio playback
- 透過 data channel 傳送 transcript deltas
- ephemeral browser credentials
- browser-specific WebRTC behavior
- unstable realtime sessions 的 failure handling

有趣的問題不是「呼叫 AI API 並翻譯文字」。

有趣的問題是建構一個 realtime browser audio pipeline，在同一個 live session 中，語音、翻譯、播放、字幕、credentials 與 WebRTC state 都必須一起協作。

## 架構

```text
Browser
├── getUserMedia()
│   └── microphone audio track
│
├── RTCPeerConnection
│   ├── sends microphone audio to OpenAI
│   ├── receives translated audio track
│   └── creates DataChannel "oai-events"
│
├── HTMLAudioElement
│   └── plays translated remote audio stream
│
└── DataChannel events
    ├── session.input_transcript.delta
    │   └── source subtitles
    └── session.output_transcript.delta
        └── translated subtitles

FastAPI backend
└── POST /session
    └── creates ephemeral OpenAI Realtime Translation client secret
```

## 運作方式

### 1. 瀏覽器擷取麥克風音訊

Frontend 透過 `navigator.mediaDevices.getUserMedia()` 要求麥克風存取權。

目前的 audio constraints 啟用：

* echo cancellation
* noise suppression
* automatic gain control

產生的 microphone track 會直接加到 WebRTC peer connection。

### 2. Backend 建立 ephemeral client secret

Frontend 不使用長期有效的 OpenAI API key。

取而代之，它呼叫本機 backend：

```text
POST /session
```

並送出：

```json
{
  "targetLanguage": "en"
}
```

接著 FastAPI server 使用 server environment 中的 `OPENAI_API_KEY` 呼叫 OpenAI 的 realtime translation client-secret endpoint。

瀏覽器只會收到 ephemeral client secret。

### 3. Frontend 執行 WebRTC exchange

Frontend：

1. 建立 `RTCPeerConnection`。
2. 加入 microphone audio track。
3. 建立 `oai-events` data channel。
4. 產生 SDP offer。
5. 使用 ephemeral client secret 將 SDP offer 送到 OpenAI。
6. 接收 SDP answer。
7. 設定 remote description。
8. 開始接收翻譯音訊與 transcript events。

### 4. 翻譯音訊作為 remote track 播放

當 OpenAI 回傳 remote media stream 時，RelAI 會把它接到 `HTMLAudioElement`，並在瀏覽器中播放翻譯後的音訊。

### 5. 字幕作為 realtime deltas 抵達

Data channel 會接收 realtime events。

RelAI 目前消費：

```text
session.input_transcript.delta
session.output_transcript.delta
```

這些 deltas 會即時附加到 UI 中，形成來源字幕與翻譯字幕。

## 模式

### Translate mode

目前啟用。

```text
microphone speech -> translated audio + source/target subtitles
```

UI 顯示：

* source transcript
* translated transcript
* translated audio playback

目標語言 selector 控制送往 backend 的輸出語言。

來源語言 selector 目前只存在於 UI；來源語音實際上由 realtime translation model 處理。

### Interpreter mode

Interpreter mode 是原本規劃的第二個模式。

設計是：

```text
Session A -> translate into language A -> left ear
Session B -> translate into language B -> right ear
```

目標是支援即時雙語口譯，使用兩個平行 translation sessions 與 stereo panning。

HTML 仍然包含 interpreter-mode UI skeleton，但目前的應用程式刻意停用它，直到單一 session translation path 穩定下來。

## 瀏覽器相容性

目前的 MVP 建議使用 Chromium-based browsers。

本機測試觀察到：

* Chromium：穩定
* Firefox / Zen Browser：可能在短時間後斷線

RelAI 會偵測 Firefox-family browsers 並顯示相容性警告。

推測問題在 WebRTC/browser behavior，而不是 UI layer。程式碼包含 WebRTC connection-state logging，並在把 soft disconnects 視為 fatal 之前給一小段 grace period。

## Stack

Frontend：

* Vite
* TypeScript
* WebRTC
* browser media APIs
* vanilla DOM UI
* CSS

Backend：

* FastAPI
* httpx
* python-dotenv
* Uvicorn

## Repository layout

```text
.
├── app
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── src
│   │   ├── main.ts
│   │   ├── style.css
│   │   └── translator.ts
│   ├── tsconfig.json
│   └── vite.config.ts
├── server
│   ├── main.py
│   └── requirements.txt
├── README.md
└── LICENSE
```

## 需求

* Python 3
* Node.js + npm
* 具有 realtime translation 存取權的 OpenAI API key
* 建議使用 Chromium-based browser 進行測試

## 本機執行

### 1. Backend

```bash
cd server
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

建立 `server/.env`：

```env
OPENAI_API_KEY=sk-...
OPENAI_SAFETY_IDENTIFIER=local-dev-user
```

執行 backend：

```bash
uvicorn main:app --reload
```

Backend 會跑在：

```text
http://localhost:8000
```

### 2. Frontend

在另一個 terminal：

```bash
cd app
npm install
npm run dev
```

開啟：

```text
http://localhost:5173
```

Vite dev server 會 proxy：

```text
/session -> http://localhost:8000
```

## Build

Frontend build：

```bash
cd app
npm run build
```

本機 preview production build：

```bash
npm run preview
```

## 安全性 notes

瀏覽器永遠不會收到長期有效的 OpenAI API key。

Credential flow 是：

```text
server/.env
    ↓
FastAPI /session
    ↓
OpenAI client-secret endpoint
    ↓
ephemeral browser secret
    ↓
WebRTC SDP exchange
```

Backend 會為了 debugging 記錄 session metadata，但刻意不印出 ephemeral secret value。

## 已知限制

* Translate mode 是唯一啟用的 mode。
* Interpreter mode 存在於 UI skeleton 中，但已停用。
* Firefox/Zen 可能在 session 開始幾秒後從 WebRTC 斷線。
* Error recovery 很基本。
* 沒有 production auth。
* 沒有 deployment config。
* 沒有 mobile wrapper。
* Source-language selection 還沒有接到 backend payload。
* UI 只是本機 MVP 測試用。

## 未來工作

可能的下一步：

* 在 single-session stability 改善後重新啟用 interpreter mode。
* 加入明確的 Web Audio routing 與 stereo panning（interpreter mode）。
* 改善 reconnect behavior。
* 更精確地記錄 Firefox/Gecko WebRTC failure mode（或嘗試解決它）。
