# qianchuan-ad-creative-workflow

A Codex/Agent skill for building Qianchuan/Douyin ad creative workflows, especially ecommerce product-card and livestream conversion creatives.

It helps an agent turn a product brief into:

- Qianchuan creative angles
- Human-style Chinese口播 scripts
- Timed subtitles
- Storyboards
- Local and network material plans
- Pexels/Pixabay/Coverr material candidates
- MiniMax TTS voiceover audio
- Review checklists and data-iteration plans

The skill is designed for two workflows:

- **Semi-auto**: the agent pauses for approval at creative,口播, material, and rough-cut stages.
- **Full-auto**: the agent proceeds from brief to draft video assets when API keys and material sources are configured.

## Repository Description

Recommended GitHub repository description:

```text
Codex skill for Qianchuan/Douyin ad creatives: product briefs,口播, storyboards, material collection, MiniMax TTS, and iteration workflows.
```

Recommended topics:

```text
codex-skill, qianchuan, douyin, ecommerce, ad-creatives, tts, minimax, pexels, pixabay, video-workflow
```

## Install

Place this folder in a skill directory used by your agent environment.

Common locations:

```text
~/.codex/skills/qianchuan-ad-creative-workflow
~/.agents/skills/qianchuan-ad-creative-workflow
<workspace>/.agents/skills/qianchuan-ad-creative-workflow
```

If cloning directly:

```bash
mkdir -p ~/.codex/skills
git clone <repo-url> ~/.codex/skills/qianchuan-ad-creative-workflow
```

Then verify:

```bash
cd ~/.codex/skills/qianchuan-ad-creative-workflow
python3 scripts/run_workflow.py --check
```

## Configure API Keys

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Fill only the services you need:

```env
PEXELS_API_KEY=
PIXABAY_API_KEY=
COVERR_API_KEY=

MINIMAX_API_KEY=
MINIMAX_GROUP_ID=
MINIMAX_TTS_MODEL=speech-02-hd
MINIMAX_TTS_VOICE_ID=Chinese (Mandarin)_Warm_Girl
```

Do not commit `.env`.

Minimum requirements:

| Workflow | Required keys |
|---|---|
| Planning only | None |
| Local materials + MiniMax voice | `MINIMAX_API_KEY` |
| Network material collection | `PEXELS_API_KEY`, `PIXABAY_API_KEY`; `COVERR_API_KEY` optional |
| Full-auto draft | `MINIMAX_API_KEY`, plus material-provider keys if using network assets |

Some MiniMax accounts require `MINIMAX_GROUP_ID`; if the request fails without it, fill it in `.env`.

## Start In Chat

Tell the agent:

```text
使用 qianchuan-ad-creative-workflow，帮我做一个千川商品卡成交素材。
```

The agent should ask you to fill:

```text
模式：全自动 / 半自动
素材来源：本地 / 网络采集 / 本地优先+网络补充
配音方式：MiniMax / 真人录音 / 暂不配音
是否加BGM：是 / 否
视频数量：1条 / 3条 / 批量
视频时长：15秒 / 30秒 / 45秒

商品/类目：
价格/优惠：
投放目标：商品卡成交 / 直播间引流 / 线索 / 复购
目标人群：
核心卖点：
真实证据：
使用场景：
已有素材路径：
禁用表达：
期望风格：
参考素材/竞品：
补充说明：
```

## Runner

The skill includes a small runner for repeatable plumbing:

```bash
python3 scripts/run_workflow.py --check
python3 scripts/run_workflow.py init-project ./my-campaign
python3 scripts/run_workflow.py collect-materials --storyboard ./my-campaign/storyboard.json --out ./my-campaign/material_candidates.json
python3 scripts/run_workflow.py tts --text ./my-campaign/voiceover.txt --out ./my-campaign/voiceover.mp3
```

The runner does not replace agent judgment. It handles setup checks, template creation, material candidate collection, and MiniMax TTS.

## Skill Contents

```text
SKILL.md
agents/openai.yaml
assets/
  brief-template.json
  storyboard-template.json
references/
  install.md
  setup.md
  prompt-starters.md
  automation-modes.md
  brief-template.md
  material-workflow.md
  voiceover-workflow.md
  iteration-rules.md
scripts/
  run_workflow.py
  material_collector.py
  minimax_tts.py
  env_loader.py
```

## Safety Notes

- Do not invent product facts, prices, certifications, results, reviews, or campaign data.
- Use local product footage for proof.
- Use network footage only for context, atmosphere, or transitions unless rights and product truth are verified.
- Treat all generated videos as drafts until a human reviews product truth, compliance, authorization, and material quality.

## License

MIT. See [LICENSE](LICENSE).

