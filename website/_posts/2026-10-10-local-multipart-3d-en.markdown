---
layout: post
title: "Local Multipart 3D: from failed raccoons to a CPU pipeline"
date: 2026-10-10 17:00:00 -0300
lang: en
project: true
permalink: /project/local-multipart-3d.html
description: "What I tried with agents, multiview reconstruction, and Blender before publishing a local image-to-3D pipeline."
---

I wanted to turn an image into a colored, editable 3D object that reasonably resembled its reference. On my computer. Without a dedicated GPU. And, if possible, without waiting half an hour every time.

The result of that process is [Local Multipart 3D](https://github.com/GCaggianese/local-multipart-3d): a pipeline combining AI planning, Hunyuan3D-2mv Turbo reconstruction on CPU, and assembly through Python and Blender.

Before that, though, there were several raccoons I would rather never see again.

## First attempt: more agents

The initial idea was to distribute the work among smaller models. One agent built in Blender, another selected bounded actions, and an independent critic reviewed the renders. A deterministic controller maintained revisions, permissions, budgets, and acceptance criteria.

Then I split the character into head, body, and tail, with parallel builders and reviewers. I also tried Three.js and stricter prompts.

The infrastructure worked. The character still looked wrong.

| Trial | Recorded time | Outcome |
|---|---:|---|
| Luna Max + Perplexity | 27m33s | Cancelled, no accepted character |
| Blender: High builder + Max judge | 24m38s | Judge approved; visual quality failed |
| Parallel Blender | 32m29s | Parts and assembly approved; I rejected the result |
| Parallel Three.js | 24m50s through the last review | Inconclusive; head still rejected |

The times end at different events, and these trials were not a controlled comparison. Three.js took 10m27s to show the first view. I did not measure a one-shot baseline from which to calculate a speedup, either.

What I could establish was practical: these workflows did not deliver an acceptable character faster. The parts were already wrong before assembly. More coordination and more reviews did not fix flat faces, strange muzzles, or mechanical limbs.

The judge could also say `READY` about something that visibly failed the requirement. A GLB that opens, has materials, and passes geometry checks can still be a bad model.

The details are in the [3D modeling report, in Spanish]({{ '/assets/local-multipart-3d/reporte-modelado-3d-es.pdf' | relative_url }}). Those trials did not establish that every small model is incapable of modeling, and I did not compare against larger models. I tried those workflows on that character, and they failed.

## Second attempt: reconstruct the silhouettes

Another line of experimentation tried to use several images of the same raccoon without a second AI model generating the geometry:

```text
Alpha PNG → silhouettes → orthographic cameras → voxels → mesh → GLB
```

I tried more views, higher resolution, tolerance for contradictions, smoothing, textures, calibration, and automatic image selection.

With synthetic shapes and known cameras, the method worked. With the generated raccoon views, fidelity remained insufficient. Angles requested from an image generator were not measured cameras, and the different views did not necessarily describe the same solid.

Two numbers from the [closure report, in Spanish]({{ '/assets/local-multipart-3d/Informe_cierre_multiview3d_ES.pdf' | relative_url }}) show the limit:

- With strict carving, increasing from 12 to 24 views reduced silhouette IoU from 0.8980 to 0.8737.
- Increasing from 128³ to 256³ voxels raised the recorded time from 3.03 to 17.34 seconds, while IoU fell from 0.9091 to 0.9062.

These are internal comparisons within that experiment. IoU measures contour overlap; on its own, it does not measure anatomy, facial relief, or asset usefulness.

The later filter reviewed 26 candidates. Fifteen passed individually, but the set failed again. There were 38 passing software tests and positive synthetic controls; the raccoon still did not meet the objective.

I closed that line of work. The code and diagnostics remained as evidence of what had not worked.

## Changing who generates the geometry

The next step was to use models trained for image-to-3D and leave interpretation, planning, and review to the LLM.

I started with TripoSR. Then I tried Hunyuan3D-2mv Turbo, which accepts multiple views for a joint reconstruction. The local raccoon test on an i7-11800H produced these results:

| Method | Generation | Peak RSS | Mean IoU over three views |
|---|---:|---:|---:|
| TripoSR, one view | 36.41s | 3.61 GiB | 0.7322 |
| Hunyuan, one view | 169.92s | 6.81 GiB | 0.7292 |
| Hunyuan, three views | 330.74s | 6.80 GiB | 0.7966 |

Each generation ran once. Times include generator startup, loading, and inference; they exclude downloads, cleanup, evaluation, and rendering. Multiview Hunyuan improved the profile and back, with a small loss at the front. It was still untextured geometry with artifacts. The [reproducible record](https://github.com/GCaggianese/local-multipart-3d/blob/main/HUNYUAN_VALIDATION.md) preserves the parameters and limits.

### The cat: geometry and color

This was the reference sheet:

![Reference sheet of the black cat, with six views]({{ '/assets/local-multipart-3d/cat_original.jpeg' | relative_url }})

These are renders of the reconstructed GLB:

![CPU-reconstructed, colored cat rendered from six angles]({{ '/assets/local-multipart-3d/cat_1.jpeg' | relative_url }})

Hunyuan received the front, both sides, and back. Generation took 480.20 seconds, roughly eight minutes, with 6.75 GiB peak RSS. For color, I also used the top and bottom views.

The black body and yellow eyes were embedded as vertex colors. Projection checks depth visibility to reduce color leaking through the object from the wrong view. Areas without coverage receive a fallback color.

That made it possible to deliver a colored GLB and render it in Blender. Projection also retains some lighting from the images; it does not automatically recover a clean physical material.

### The motorcycle: where the limit becomes visible

The reference was a single photograph:

![Reference photograph of a black sportbike]({{ '/assets/local-multipart-3d/bike_original.jpeg' | relative_url }})

I generated six views with Codex and used four for Hunyuan. Surfaces hidden in the photograph were inferred. These are renders of the first reconstruction:

![First multiview motorcycle reconstruction, with projected colors]({{ '/assets/local-multipart-3d/bike_1-fast.jpeg' | relative_url }})

Geometry took 8m34s, with 6.75 GiB peak RSS. That time excludes image generation and prior weight downloads.

The overall shape is recognizable. So are the ripples in the fairings, fused details, and soft shapes. Some reflections were interpreted as surface relief.

I then rebuilt the motorcycle from scratch with procedural geometry in Blender, organized into 20 editable assemblies: wheels, brakes, forks, handlebars, panels, and exhaust.

![Motorcycle rebuilt from scratch with procedural geometry and Blender materials]({{ '/assets/local-multipart-3d/bike_2.jpeg' | relative_url }})

**This second motorcycle is a specific Blender build.** It is not an automatic Local Multipart 3D output or a refinement of the earlier Hunyuan mesh. It has separate materials and more controllable mechanical shapes; the fairings and hidden details remain an interpretation of the reference.

I then ran another trial: reconstructing the same 20 parts with TripoSR, using isolated renders of the procedural version as inputs. The full workflow took 17m24s, including preparation, inspection, and retries. The procedural version looked better; the neural model softened and distorted parts again.

Decomposition helped control the object, but each generated part added work. There was no reason to ask a network to reinvent a cylinder or wheel every time.

## What ended up in the repository

Local Multipart 3D combines neural reconstruction, primitives, and Blender helpers according to the object's needs. The planner chooses the decomposition; there is no “always twenty parts” rule. A connected sculpted form can stay whole. A repeated piece can be generated once and instantiated several times.

The current flow is:

```text
Image or prompt
  → planning and JSON recipe
  → multiview atlas per part
  → CPU Hunyuan reconstruction + procedural geometry
  → color projection
  → Blender assembly and renders
  → per-view observations + whole-assembly review
  → bounded correction, export, and checks
```

The default policy uses Luna high for interpretation, decomposition, and view observations; Sol 6.1 medium reviews the assembly and proposes one correction recipe. Python validates and executes those decisions. Observations can run in parallel, while corrections have one owner.

Jobs save their stages and results. If something fails after a part has been generated, the job can resume without repeating all inference. Outputs include `.glb`, editable `.blend`, atlas, recipe, renders, and reports.

Geometry, color, and Blender run locally. Planning, images, and review use the Codex session: the complete workflow needs online access. “On CPU” describes the 3D reconstruction.

There were also remote trials of a lantern and a mask. The mask took 6m31s from retry to result, including one regeneration. That number belongs to the remote Hunyuan 3.1 Rapid backend. The [gallery](https://github.com/GCaggianese/local-multipart-3d/blob/main/docs/GALLERY.md) keeps those examples separate from the local backend.

## The full test: a fountain pen

To test the repository on its own, I ran a fountain pen without manually editing the recipe or modeling its parts by hand. The first attempt failed before geometry generation: the repair prompt requested colors in `0–1`, while the schema expected bytes in `0–255`. I fixed that contradiction and repeated the job.

![Fountain pen reference and result from the repository's local workflow]({{ '/assets/local-multipart-3d/pen-comparison.png' | relative_url }})

The second attempt generated the body, nib, and detached cap, using one CPU worker:

- **17m48s** to the first valid export.
- **29m55s** to completion, including two regenerations.

Exports passed local checks. The nib, threads, clip, and emblem remained simplified. Visual status stayed `unverified_after_correction`: passing checks after a correction does not imply a new visual approval.

Under ten minutes remains a target for small jobs. The [pen evidence](https://github.com/GCaggianese/local-multipart-3d/blob/main/evidence/pen-benchmark.json) shows how long one complete local job actually took.

## Try it

The repository contains setup scripts, code, a decomposition skill, and the [full guide](https://github.com/GCaggianese/local-multipart-3d/blob/main/GUIDE.md). It requires Linux, Python, host Blender, and an authenticated Codex session; initial setup downloads the weights.

With the environment prepared, submit a local job like this:

```bash
.venv-orchestrator/bin/python -m app.multipart.cli submit \
  --root outputs/local-jobs --profile local-cpu \
  --images /absolute/path/reference.png \
  --instruction "Create a colored 3D asset matching the reference" \
  --ai-policy luna-sol --cpu-workers 2 --cpu-threads 8 \
  --submission-limit 6 --max-estimated-usd 0 --run
```

Each user can choose the worker count and threads per inference. Memory and thread-budget guards apply; two processes share CPU and bandwidth, so parallelism needs measuring on each machine. To start from text, omit `--images`.

The project's code and documentation are published under Apache-2.0, with REUSE metadata. External models and references retain their respective rights.

What I have from this work is a pipeline I can run, inspect, and resume. Also a stricter standard for reading its results: opening a file, passing tests, and recognizing an object are different achievements from reproducing the reference well.

## Reports and sources

- [More agents, no better result — Spanish PDF]({{ '/assets/local-multipart-3d/reporte-modelado-3d-es.pdf' | relative_url }}).
- [Silhouette reconstruction closure report — Spanish PDF]({{ '/assets/local-multipart-3d/Informe_cierre_multiview3d_ES.pdf' | relative_url }}).
- [Local Multipart 3D code, guide, and gallery](https://github.com/GCaggianese/local-multipart-3d), checked when publishing this post.

The cat and motorcycle images document trials preceding the packaged workflow. The pen documents a run of the published implementation. References are shown for comparison; their inclusion grants no rights to third-party photographs or designs. Reference and output cameras and lighting differ.
