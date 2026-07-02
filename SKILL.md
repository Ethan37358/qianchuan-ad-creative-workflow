---
name: qianchuan-ad-creative-workflow
description: Create Qianchuan/Douyin ad creative workflows for ecommerce and livestream conversion. Use when the user wants 千川投放素材, 巨量千川创意, 抖音广告口播, 直播间引流脚本, 商品卡成交素材, ad script matrices, storyboard/material plans, compliance-aware口播 variants,素材采集 planning, batch video production planning, or post-campaign creative iteration from CTR/CVR/ROI data.
---

# Qianchuan Ad Creative Workflow

## Core Rule

Build a production workflow, not just a script. For Qianchuan work, always connect:

```text
product truth -> audience pain -> sellable claim ->口播 -> storyboard -> materials -> edit variants -> review -> test plan -> data iteration
```

Do not invent product facts, prices, certifications, results, inventory, endorsements, or campaign data. Ask for missing facts or mark them as assumptions. Treat compliance review as required before launch.

## Intake

Start by collecting or normalizing a product brief. If the user gives incomplete information, proceed with clearly labeled assumptions and request the highest-risk missing items.

Required fields:

- Product/category
- Price, offer, or直播间 mechanism
- Target audience
- Primary conversion goal: livestream entry, 商品卡成交, lead collection, or retargeting
- Real selling points and proof
- Usage scenes
- Existing materials: product shots, livestream clips, UGC, reviews, comparison footage, screenshots
- Forbidden claims, sensitive words, compliance limits
- Platform and format: Douyin/Qianchuan, usually 9:16

Read `references/brief-template.md` when a structured brief is needed.
Read `references/setup.md` when the user asks where to put API keys, how to run on another computer, or how to configure external providers.
Read `references/install.md` when the user asks how to install this skill from GitHub or move it to another computer.
Read `references/prompt-starters.md` when the user invokes the skill without providing a full brief; send the standard intake form before doing creative work.

## Automation Modes

Always identify the user's preferred mode at intake:

- **Full-auto mode**: proceed from brief to finished draft video without stopping for intermediate approval. Use this only for testing, rough drafts, or when the user explicitly accepts that facts, material fit, and compliance still need final human review.
- **Semi-auto mode**: generate each major module and pause for user approval before the next production step. Use this by default for real Qianchuan launch material.

Read `references/automation-modes.md` when building or running an end-to-end workflow.

## Workflow

### 1. Diagnose Product And Conversion Path

Summarize:

- Who buys and why now
- Top 3 pain points
- Top 3 believable selling points
- Proof available for each selling point
- What the ad should make users do next
- What must not be said

If the product depends on health, finance, education, cosmetics, medical devices, income claims, or strong before/after claims, add a stricter compliance warning and avoid absolute outcomes.

### 2. Build Creative Matrix

Create a matrix with 5-10 creative angles. Prefer these angle families:

- Pain-point opening
- Avoid-mistake / anti-pitfall
- Real usage scene
- Comparison without illegal absolute claims
- Live-room mechanism / today-only benefit when verified
- Buyer feedback when evidence is provided
- Product demonstration
- Expert/consultant explanation only when credentials are verified
- Boss/founder explanation
- Price-value logic

For each angle include:

- Target audience
- Hook
- Core claim
- Required proof/material
- Risk level
- Best conversion path

### 3. Generate口播 As A Separate Module

Do not bury口播 inside generic script output. Generate mouth-friendly variants:

- 真人口播版: conversational, can be read by主播/达人/员工
- AI配音版: shorter sentences, clean rhythm, minimal口头禅
- 直播间引流版: motivates room entry and live demonstration
- 商品卡成交版: motivates product card click and purchase
- Subtitle-cut version: 1 short line per beat

Each口播 should include:

- First 3 seconds hook
- Problem or scenario
- Product entry
- 1-3 verified selling points
- Proof or demonstration cue
- Conversion action
- Compliance note if needed

Avoid fake urgency, guaranteed outcomes, fake user identity, unverified awards, medical/financial promises, and extreme words unless the user proves they are allowed.

For video automation, generate both:

- **Voiceover script**: timed, readable aloud, controlled to the target duration.
- **Subtitle script**: shorter and punchier than the spoken script.

Read `references/voiceover-workflow.md` for真人感口播, TTS selection, pacing, and background audio rules.

### 4. Create Storyboard And Material Needs

Turn selected口播 into a shot table:

- Scene number
- Time range
- Voiceover line
- Visual action
- Material type
- Existing source or acquisition source
- Search keywords in Chinese and English
- AI image/video prompt if generated material is suitable
- Must-show product detail
- Compliance risk

Read `references/material-workflow.md` for acquisition and folder structure.

Support two material modes:

- **Local material mode**: scan and match a user-provided folder.
- **Network acquisition mode**: generate search terms and collect/prepare candidates from stock/video sources when network tools and rights allow it.

When an existing material folder is provided, first create a material inventory before final shot binding:

- Count videos/images by folder.
- Identify folder names that imply tested creative directions, such as 材质安全, 立减, 免费试睡, 信息流, 直播切片, 口播, 结构, 商品图.
- Extract or generate preview thumbnails/contact sheets when possible.
- Check duration and orientation metadata when available.
- Bind only likely usable candidates to each scene and mark uncertainty if the visual content has not been reviewed.

### 5. Plan Batch Variants

Produce variants intentionally. Do not make 20 random videos.

Common test axes:

- Hook: pain vs pitfall vs benefit vs scene
- Speaker: buyer vs主播 vs boss vs consultant
- Conversion path: live room vs product card
- Material type: real product shot vs livestream clip vs UGC-style demo
- Duration: 15s vs 30s

Name variants with a compact convention:

```text
商品_角度_人设_路径_时长_版本
```

Example:

```text
保温杯_避坑_主播_直播间_15s_A1
```

### 6. Review Before Launch

Before recommending launch, produce an audit checklist:

- Product facts match the brief
- No unverified claims
- No forbidden words
- Price/offer matches current campaign
- Voiceover and visual match
- Subtitles are readable
- Product appears clearly
- No watermark/copyright issue
- Conversion action is clear
- Landing/live-room承接 is consistent

### 7. Iterate From Data

When the user provides campaign data, analyze creative-level performance before account-level advice. Use:

- CTR: hook and visual attraction
- 3s/5s retention or watch time: opening and pacing
- Click-to-live-room or product click rate: conversion intent
- CVR: offer, trust, page/live-room承接
- CPA/ROI: commercial viability
- Comments/negative feedback: claim mismatch or trust issue

Read `references/iteration-rules.md` for diagnosis rules.

## Output Formats

For a full task, output these sections:

1. Product And Risk Assumptions
2. Audience And Pain Points
3. Creative Matrix
4.口播 Variants
5. Storyboard And Material Needs
6. Batch Test Plan
7. Review Checklist
8. Next Inputs Needed

For quick tasks, output only the requested module but preserve compliance notes and assumptions.

## Automation Boundary

Automate generation, organization,素材需求, draft editing plans, and first-pass analysis. Keep the user in the loop for:

- Product truth
- Creative direction selection
-口播 approval
- Material approval
- Compliance and launch approval
- Budget and scaling decisions

MoneyPrinterTurbo or FFmpeg-style video assembly can be used later as an execution engine, but this skill should remain tool-agnostic: first produce structured creative inputs that can feed 剪映, CapCut, MoneyPrinterTurbo, AI video tools, or a custom pipeline.

## Bundled Scripts

Use `scripts/run_workflow.py` as the unified entrypoint for configuration checks, project initialization, network material collection, and MiniMax TTS. It does not replace agent judgment; use it for repeatable plumbing after creative decisions are made.

Use `scripts/material_collector.py` when the workflow needs network素材候选 from Pexels, Pixabay, or Coverr. It reads storyboard JSON, uses `PEXELS_API_KEY`, `PIXABAY_API_KEY`, and optional `COVERR_API_KEY`, and outputs a candidate JSON. Use local materials for product-proof scenes and network materials for context/atmosphere.

Use `scripts/minimax_tts.py` when the workflow needs MiniMax口播音频. It reads voiceover text, uses `MINIMAX_API_KEY` and `MINIMAX_GROUP_ID`, and writes mp3 audio. Use system TTS only for local pipeline tests; use MiniMax or uploaded human recording for production-like drafts.
