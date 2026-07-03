# Automation Modes

Use this reference when the user wants the workflow to behave as a system rather than a one-off plan.

## Mode Selection

Ask or infer one of:

```text
模式：全自动 / 半自动
素材来源：本地素材 / 网络采集 / 本地优先+网络补充
口播方式：真人稿 / 系统TTS测试 / 商业TTS / 用户上传录音
输出：方案文档 / 粗剪视频 / 带口播视频 / 批量版本
```

If the user does not specify, default to semi-auto for real launch work and full-auto for technical tests.

## Full-Auto Mode

Goal: generate a rough video draft from the brief without pausing.

Flow:

```text
brief
-> assumptions and risk map
-> creative angle selection
-> timed voiceover
-> subtitle cuts
-> storyboard
-> material acquisition/matching
-> auto scene binding
-> TTS or uploaded voiceover
-> background music/room tone selection
-> video assembly
-> preview sheet
-> final review checklist
```

Rules:

- Pick the lowest-risk creative angle when uncertain.
- Prefer product-visible footage over abstract or stock visuals.
- If a claim lacks proof, downgrade wording automatically.
- Mark all uncertain assumptions in the final report.
- Produce a review checklist even when the user requested full automation.

Full-auto output should include:

- Draft video
- Voiceover text
- Subtitle text
- Material binding table
- Preview sheet
- Risks and assumptions

## Semi-Auto Mode

Goal: keep human judgment at key points.

Flow and approval gates:

```text
1. Brief normalization -> user confirms product facts
2. Creative matrix -> user chooses 1-3 directions
3. Voiceover variants -> user approves口播
4. Material candidates -> user approves visuals
5. Rough cut -> user reviews pacing and fit
6. Final package -> user approves launch/re-edit
```

Use semi-auto when:

- The material is intended for real ad launch.
- Product claims are sensitive.
- The product category is regulated.
- User cares about brand tone and visual quality.
- Existing materials are messy or mixed with unrelated tests.

## Batch Generation

For batch work, do not randomize everything. Vary one or two axes per batch:

- Hook
- Speaker/persona
- Material source
- CTA
- Duration
- Selling point order

Recommended first batch:

```text
A1: pain/pitfall hook
B1: material trust hook
C1: structure demonstration hook
```

After performance data arrives, expand only the winning axis.

