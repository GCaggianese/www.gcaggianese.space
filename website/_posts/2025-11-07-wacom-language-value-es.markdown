---
layout: post
title: "Wacom en GNU Guix"
date: 2025-11-07 21:12:39 -0300
lang: es
resource-guix: true
permalink: /resource/wacom.html
---

-   Usar `xinput list` para revisar cómo la está manejando el sistema.

> Traducción de <a {% static_href %}href="/resource/wacom.html"{% endstatic_href %}>la publicación original en inglés</a>.

    -   En mi caso:

            ~
            ❯ xinput list
            ⎡ Virtual core pointer                      id=2    [master pointer  (3)]
            ⎜   ↳ Wacom Intuos S Pen Pen (0xb819f76)        id=27   [slave  pointer  (2)]
            ⎣ Virtual core keyboard                     id=3    [master keyboard (2)]
                ↳ Wacom Intuos S Pen                        id=26   [slave  keyboard (3)]

-   Listar sus propiedades por ID.

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

-   Asignarla a la pantalla X11 deseada. En mi caso, el `input ID` de
    la tableta es `27` y mi pantalla X11 es `HDMI-1`.

    ``` bash
    xinput map-to-output 27 HDMI-1
    ```

