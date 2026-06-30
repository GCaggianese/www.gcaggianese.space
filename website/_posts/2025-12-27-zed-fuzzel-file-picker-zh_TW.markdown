---
layout: post
title: "zed-fuzzel-filepicker"
date: 2025-12-27 01:56:19 -0300
lang: zh_TW
permalink: /project/zed-fuzzel-filepicker.html
---

這是一個給 Zed editor 使用的遞迴 fuzzy file picker，使用 Fuzzel，靈感來自 Emacs 的 dired 導航。

> 本文翻譯自<a {% static_href %}href="/project/zed-fuzzel-filepicker.html"{% endstatic_href %}>英文原文</a>。

**Github**: *[GCaggianese/zed-fuzzel-filepicker](https://github.com/GCaggianese/zed-fuzzel-filepicker.git)*

## 功能

用 fuzzy search 和遞迴目錄導航瀏覽並開啟檔案。
按下 keybind 後搜尋檔案，並直接在 Zed 裡由 Zed 開啟它們。

## 為什麼

我開始試用 Zed 時，第一個想念的是 dired 的 file picker。這個專案試著把那個缺口補到 Zed 裡。

## Demo

![demo](../assets/zed-fuzzel-filepicker.gif)

## 需求

- [Zed editor](https://zed.dev/) 與 `zeditor` CLI tool
- [Fuzzel](https://codeberg.org/dnkl/fuzzel)（或 rofi/dmenu；見調整段落）
- [fd](https://github.com/sharkdp/fd)（比 `find` 更快的替代品）
- 任意 Unix-like 系統

## 安裝

### 1. 安裝依賴

```bash
# Arch
sudo pacman -S fuzzel fd zed

# Debian (zed via official install)
sudo apt install fuzzel fd-find
```

### 2. 設定 script

```bash
# Copy script to your local bin
cp fuzzel-file-picker ~/.local/bin/
chmod +x ~/.local/bin/fuzzel-file-picker
```

### 3. 設定 Zed

**加入 `tasks.json`** (`~/.config/zed/tasks.json`)：

```json
[
  {
    "label": "file-picker",
    "command": "~/.local/bin/fuzzel-file-picker \"${ZED_DIRNAME:-$ZED_WORKTREE_ROOT}\" > /dev/null 2>&1",
    "use_new_terminal": false,
    "reveal": "never",
    "hide": "always",
    "show_summary": false,
    "show_command": false
  }
]
```

**加入 `keymap.json`** (`~/.config/zed/keymap.json`)：

```json
{
  "bindings": {
    "space .": ["task::Spawn", { "task_name": "file-picker" }]
  }
}
```

*（把 `space .` 換成你想要的 keybind。）*

## 使用

1. **在專案中開啟 Zed**
2. **按 `Space + .`**（或你的 keybind）
3. **導航：**
   - 輸入以 fuzzy-search 檔案/目錄
   - 選擇 `..` 回到上一層
   - 選擇目錄進入更深層
   - 選擇檔案並在 Zed 中開啟
   - 也可以建立新檔案
4. **Esc 可隨時取消**

## 運作方式

- 使用 `fd` 列出檔案/目錄
- Fuzzel 提供 fuzzy-search 介面
- 遞迴瀏覽目錄直到選擇或建立檔案
- 透過 `zeditor` CLI 開啟選取的檔案

### 使用不同 launcher

我猜可以把 `fuzzel --dmenu` 換成：
- **rofi:** `rofi -dmenu -p`
- **dmenu:** `dmenu -p`
- **fzf:** `fzf --prompt`

但我還沒試過。

## 從 Zed 整合

這個模式可以透過 tasks 把**任何外部工具**整合進 Zed：

1. 寫一個輸出到 stdout/stderr 的 script
2. 在 `tasks.json` 加入 task 並重導輸出
3. 在 `keymap.json` 將 task 綁到 keybind

這很酷，因為它讓 Zed 很容易被擴充。

## Troubleshooting

**"zeditor: command not found"**
- 安裝 Zed CLI：開啟 Zed -> `Cmd/Ctrl+Shift+P` -> "Install CLI"

**"fd: command not found"**
- 某些系統中 `fd` 名稱不同，需要依你的系統調整 script。

---

## 問題 / bugs？想要改造它？

開 issue 或 PR。想怎麼 hack 都可以。
如果你用這個 task integration pattern 做其他工具，我很想看看你做了什麼。可以在 issues 留連結或 tag 這個 repo。能建立一組 Zed integrations 會很棒。

