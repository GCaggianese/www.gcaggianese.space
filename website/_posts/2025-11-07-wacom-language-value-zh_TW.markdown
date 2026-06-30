---
layout: post
title: "在 GNU Guix 上使用 Wacom"
date: 2025-11-07 21:12:39 -0300
lang: zh_TW
resource-guix: true
permalink: /resource/wacom.html
---

-   使用 `xinput list` 檢查系統如何處理它。

> 本文翻譯自<a {% static_href %}href="/resource/wacom.html"{% endstatic_href %}>英文原文</a>。

    -   以我的情況為例：

            ~
            ❯ xinput list
            ⎡ Virtual core pointer                      id=2    [master pointer  (3)]
            ⎜   ↳ Wacom Intuos S Pen Pen (0xb819f76)        id=27   [slave  pointer  (2)]
            ⎣ Virtual core keyboard                     id=3    [master keyboard (2)]
                ↳ Wacom Intuos S Pen                        id=26   [slave  keyboard (3)]

-   依照 ID 列出它的屬性。

        ~
        ❯ xinput list-props 26
        Device 'Wacom Intuos S Pen':
          Device Enabled (187):   1
          Coordinate Transformation Matrix (189): 1.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 1.000000
          libinput Calibration Matrix (1206): 1.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 1.000000
          libinput Calibration Matrix Default (1207): 1.000000, 0.000000, 0.000000, 0.000000, 1.000000, 0.000000, 0.000000, 0.000000, 1.000000
          libinput Send Events Modes Available (304): 1, 0
          libinput Send Events Mode Enabled (305):    0, 0
          libinput Send Events Mode Enabled Default (306):    0, 0
          Device Node (307):  "/dev/input/event25"
          Device Product ID (308):    1386, 884

-   把它映射到想要的 X11 顯示器。我的情況中，平板的 `input ID`
    是 `27`，X11 顯示器是 `HDMI-1`。

    ``` bash
    xinput map-to-output 27 HDMI-1
    ```

