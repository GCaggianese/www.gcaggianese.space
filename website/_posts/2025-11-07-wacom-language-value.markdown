---
layout: post
title: "Wacom on GNU Guix"
date: 2025-11-07 21:12:39 -0300
lang: en
resource-guix: true
permalink: /resource/wacom.html
---

-   Use `xinput list` to check how is it beign handled by the system

    -   In my case:

            ~
            ❯ xinput list
            ⎡ Virtual core pointer                      id=2    [master pointer  (3)]
            ⎜   ↳ Wacom Intuos S Pen Pen (0xb819f76)        id=27   [slave  pointer  (2)]
            ⎣ Virtual core keyboard                     id=3    [master keyboard (2)]
                ↳ Wacom Intuos S Pen                        id=26   [slave  keyboard (3)]

-   List it's properties by ID

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

-   Set it to the X11 desired Display In my case the `input ID` of the
    tablet is `27` and my X11 Display HDMI-1

    ``` bash
    xinput map-to-output 27 HDMI-1
    ```
