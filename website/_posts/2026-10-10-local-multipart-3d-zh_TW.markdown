---
layout: post
title: "Local Multipart 3D：從失敗的浣熊到 CPU 上的 pipeline"
date: 2026-10-10 17:00:00 -0300
lang: zh_TW
project: true
permalink: /project/local-multipart-3d.html
description: "在發布本機 image-to-3D pipeline 之前，我用 agents、多視角重建與 Blender 做了哪些實驗。"
---

我想把一張圖片變成有顏色、可以編輯，而且跟參考圖有一定相似度的 3D 物件。在自己的電腦上跑。不需要獨立 GPU。如果可以，也不用每次都等半小時。

這段過程最後變成了 [Local Multipart 3D](https://github.com/GCaggianese/local-multipart-3d)：把 AI 規劃、CPU 上的 Hunyuan3D-2mv Turbo 重建，以及 Python／Blender 組裝接在一起的 pipeline。

不過，在那之前，我看過好幾隻實在不想再看到的浣熊。

## 第一個嘗試：更多 agents

最初的想法是把工作分給比較小的模型。一個 agent 在 Blender 裡建模，另一個選擇範圍有限的操作，獨立的 critic 檢查 renders。確定性的 controller 負責保存版本、權限、預算與驗收條件。

後來我把角色拆成頭、身體和尾巴，讓建模與審查並行執行。也試了 Three.js 和更嚴格的 prompts。

基礎設施可以運作。角色還是長得不對。

| 實驗 | 記錄時間 | 結果 |
|---|---:|---|
| Luna Max + Perplexity | 27 分 33 秒 | 取消，沒有通過驗收的角色 |
| Blender：High 建模 + Max 評審 | 24 分 38 秒 | 評審批准，但視覺品質失敗 |
| Blender 並行建模 | 32 分 29 秒 | 零件與整體都獲批准；我拒絕了結果 |
| Three.js 並行建模 | 到最後一次審查為止 24 分 50 秒 | 未完成；頭部仍被退回 |

這些時間停在不同的事件，實驗也不是受控比較。Three.js 花了 10 分 27 秒才顯示第一個視角。我也沒有測量 one-shot baseline，所以無法計算加速倍率。

可以確認的是實際結果：這些流程沒有更快地給我一個合格角色。零件在組裝之前就已經有問題。更多協調和審查，沒有修好扁平的臉、奇怪的口鼻與機械式的四肢。

評審還可能對明顯不符合要求的模型說 `READY`。GLB 能開啟、有材質、通過幾何檢查，仍然可能是一個很差的模型。

細節保存在[西班牙文 3D 建模報告]({{ '/assets/local-multipart-3d/reporte-modelado-3d-es.pdf' | relative_url }})。這些實驗沒有證明所有小模型都不能建模，也沒有跟更大的模型比較。我測的是這些流程與這個角色，而它們失敗了。

## 第二個嘗試：從輪廓重建

另一條實驗路線想利用同一隻浣熊的多張圖片，不使用第二個 AI 模型來生成幾何：

```text
帶 alpha 的 PNG → 輪廓 → 正交相機 → voxels → mesh → GLB
```

我試了更多視角、更高解析度、容許視角互相矛盾、平滑化、貼圖、校準與自動圖片篩選。

在合成形狀與已知相機上，方法可以運作。換成生成的浣熊圖片，還原程度仍然不夠。向圖片生成器要求的角度，不是實際測量過的相機；不同圖片也不一定描述同一個立體物件。

[西班牙文結案報告]({{ '/assets/local-multipart-3d/Informe_cierre_multiview3d_ES.pdf' | relative_url }})裡的兩組數字顯示了限制：

- 嚴格 carving 下，從 12 個視角增加到 24 個視角，輪廓 IoU 由 0.8980 降到 0.8737。
- 從 128³ 增加到 256³ voxels，記錄時間由 3.03 秒增加到 17.34 秒，IoU 卻由 0.9091 降到 0.9062。

這些是該實驗內部的比較。IoU 衡量輪廓重疊，單靠它無法衡量解剖、臉部起伏或 asset 是否有用。

後來的篩選器檢查了 26 張候選圖片。15 張個別通過，但整組再次失敗。38 個軟體測試通過，合成對照也有正面結果；浣熊還是沒有達到目標。

我結束了這條路線。程式與診斷資料留下來，記錄哪些方法沒有成功。

## 改變生成幾何的角色

下一步是用專門訓練來做 image-to-3D 的模型，把理解、規劃和審查交給 LLM。

我先用了 TripoSR，接著測 Hunyuan3D-2mv Turbo。後者可以把多個視角一起用來重建。浣熊在本機 i7-11800H 上的結果如下：

| 方法 | 生成時間 | 峰值 RSS | 三個視角的平均 IoU |
|---|---:|---:|---:|
| TripoSR，單一視角 | 36.41 秒 | 3.61 GiB | 0.7322 |
| Hunyuan，單一視角 | 169.92 秒 | 6.81 GiB | 0.7292 |
| Hunyuan，三個視角 | 330.74 秒 | 6.80 GiB | 0.7966 |

每種生成只執行一次。時間包含生成器啟動、載入與推論，不含下載、清理、評估與渲染。多視角 Hunyuan 改善了側面與背面，正面稍微變差。它仍然是沒有貼圖、帶有瑕疵的幾何。[可重現的記錄](https://github.com/GCaggianese/local-multipart-3d/blob/main/HUNYUAN_VALIDATION.md)保留了參數與限制。

### 貓：幾何與顏色

這是參考圖：

![黑貓的六視角參考圖]({{ '/assets/local-multipart-3d/cat_original.jpeg' | relative_url }})

這些則是重建 GLB 的 renders：

![在 CPU 上重建並上色的黑貓，從六個角度渲染]({{ '/assets/local-multipart-3d/cat_1.jpeg' | relative_url }})

Hunyuan 收到正面、左右兩側與背面。生成花了 480.20 秒，約八分鐘，峰值 RSS 為 6.75 GiB。上色還使用了頂面與底面。

黑色身體與黃色眼睛以 vertex colors 存入模型。投影時會檢查深度可見性，減少錯誤視角的顏色穿透物件。沒有圖片覆蓋的區域使用備用顏色。

因此可以交付有顏色的 GLB，並在 Blender 裡渲染。不過，投影也保留了圖片中的部分光照，不會自動還原出乾淨的物理材質。

### 摩托車：限制變得明顯

參考只有一張照片：

![黑色跑車摩托車的參考照片]({{ '/assets/local-multipart-3d/bike_original.jpeg' | relative_url }})

我用 Codex 生成六個視角，其中四個送入 Hunyuan。照片看不到的表面是推測出來的。這是第一版重建的 renders：

![第一版多視角摩托車重建，使用投影顏色]({{ '/assets/local-multipart-3d/bike_1-fast.jpeg' | relative_url }})

幾何生成花了 8 分 34 秒，峰值 RSS 為 6.75 GiB。這個時間不包含圖片生成與先前的權重下載。

整體外形可以辨認。整流罩上的波紋、黏在一起的細節與軟化的形狀也很明顯。有些反光被解讀成了表面起伏。

接著我在 Blender 裡從零用 procedural geometry 重做摩托車，分成 20 個可編輯組件：輪胎、煞車、前叉、把手、面板、排氣管。

![以 procedural geometry 與 Blender 材質從零重做的摩托車]({{ '/assets/local-multipart-3d/bike_2.jpeg' | relative_url }})

**這第二台摩托車是針對該參考製作的 Blender 模型。** 它不是 Local Multipart 3D 的自動輸出，也不是修改前一版 Hunyuan mesh 得到的。它有分開的材質與更容易控制的機械形狀；整流罩與隱藏細節仍然是對參考的詮釋。

之後我又做了一個實驗：以 procedural 版本的各零件獨立 renders 當輸入，讓 TripoSR 重建同樣的 20 個零件。整個 workflow 花了 17 分 24 秒，包含準備、檢查與重試。Procedural 版本看起來更好；神經模型又把零件軟化、變形了。

拆分有助於控制物件，但每個生成零件都增加工作。沒有理由每次都請神經網路重新發明圓柱或輪子。

## 最後放進 repository 的流程

Local Multipart 3D 按照物件需求，混合神經重建、primitives 和 Blender helpers。由 planner 決定怎麼拆，不是「永遠二十個零件」。連在一起的雕塑形狀可以保留為一整塊。重複零件可以生成一次，再建立多個 instances。

目前流程如下：

```text
圖片或 prompt
  → 規劃與 JSON recipe
  → 每個零件的多視角 atlas
  → CPU Hunyuan 重建 + procedural geometry
  → 顏色投影
  → Blender 組裝與 renders
  → 各視角觀察 + 整體審查
  → 有限修正、匯出與檢查
```

預設策略用 Luna high 理解輸入、拆分零件與觀察各視角；Sol 6.1 medium 審查整體，提出一份修正 recipe。Python 驗證並執行這些決定。觀察可以並行，但修正由單一角色統一提出。

每個 job 都保存階段與結果。某個零件生成完成後，如果後續步驟失敗，可以接續執行，不用重跑所有推論。輸出包含 `.glb`、可編輯的 `.blend`、atlas、recipe、renders 與報告。

幾何、顏色和 Blender 都在本機執行。規劃、圖片與審查使用 Codex session，完整 workflow 需要網路。「在 CPU 上」指的是 3D 重建。

也做過燈籠和面具的遠端實驗。面具從重試到結果花了 6 分 31 秒，包含一次重新生成。這個數字屬於遠端 Hunyuan 3.1 Rapid backend。[Gallery](https://github.com/GCaggianese/local-multipart-3d/blob/main/docs/GALLERY.md)把這些範例與本機 backend 分開標示。

## 完整測試：一支鋼筆

為了測試 repository 本身，我跑了一支鋼筆，不手動修改 recipe，也不手工建模。第一次在生成幾何之前就失敗：修復 prompt 要求顏色用 `0–1`，但 schema 預期的是 `0–255` 的 bytes。我修正這個矛盾，再執行一次。

![鋼筆參考與 repository 本機 workflow 的結果]({{ '/assets/local-multipart-3d/pen-comparison.png' | relative_url }})

第二次生成了筆身、筆尖與分離的筆蓋，使用一個 CPU worker：

- **17 分 48 秒**得到第一個有效 export。
- **29 分 55 秒**完成，包含兩次重新生成。

Exports 通過本機檢查。筆尖、螺紋、筆夾與徽記仍然被簡化。視覺狀態保留為 `unverified_after_correction`：修正後通過檢查，不代表已取得新的視覺批准。

十分鐘以內仍然是小型工作的目標。[鋼筆測試資料](https://github.com/GCaggianese/local-multipart-3d/blob/main/evidence/pen-benchmark.json)記錄了一個完整本機工作實際需要的時間。

## 試著執行

Repository 包含安裝 scripts、程式碼、拆分 skill 與[完整指南](https://github.com/GCaggianese/local-multipart-3d/blob/main/GUIDE.md)。需要 Linux、Python、host Blender 與已登入的 Codex；初次 setup 會下載模型權重。

環境準備好之後，可以這樣提交本機工作：

```bash
.venv-orchestrator/bin/python -m app.multipart.cli submit \
  --root outputs/local-jobs --profile local-cpu \
  --images /absolute/path/reference.png \
  --instruction "依照參考建立有顏色的 3D asset" \
  --ai-policy luna-sol --cpu-workers 2 --cpu-threads 8 \
  --submission-limit 6 --max-estimated-usd 0 --run
```

使用者可以選 worker 數量與每次推論的 threads。程式有記憶體與執行緒預算檢查；兩個 process 共享 CPU 與頻寬，所以需要在各自電腦上測量並行效果。從文字開始時，省略 `--images`。

專案程式碼與文件以 Apache-2.0 發布，附有 REUSE metadata。外部模型與參考圖保留各自的權利。

這次工作留下了一個我能執行、檢查與接續的 pipeline。也讓我對結果有更嚴格的判準：檔案能開啟、tests 通過、物件能辨認，和忠實重現參考，是不同的成果。

## 報告與來源

- [更多 agents，沒有更好的結果 — 西班牙文 PDF]({{ '/assets/local-multipart-3d/reporte-modelado-3d-es.pdf' | relative_url }})。
- [輪廓重建結案報告 — 西班牙文 PDF]({{ '/assets/local-multipart-3d/Informe_cierre_multiview3d_ES.pdf' | relative_url }})。
- [Local Multipart 3D 程式碼、指南與 gallery](https://github.com/GCaggianese/local-multipart-3d)，於發布本文時核對。

貓與摩托車圖片記錄的是 workflow 打包之前的實驗。鋼筆記錄的是已發布實作的一次執行。參考圖僅供比較，刊載不授予第三方照片或設計的權利。參考與結果的相機及光照不同。
