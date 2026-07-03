# Install

Use this when installing the skill from GitHub or moving it to a new computer.

## Folder Placement

Place the whole `qianchuan-ad-creative-workflow` folder inside the local skills directory used by the agent environment.

Common locations:

```text
~/.codex/skills/qianchuan-ad-creative-workflow
~/.agents/skills/qianchuan-ad-creative-workflow
<workspace>/.agents/skills/qianchuan-ad-creative-workflow
```

Keep the folder name exactly:

```text
qianchuan-ad-creative-workflow
```

## Install From GitHub

```bash
git clone <repo-url>
mkdir -p ~/.codex/skills
cp -R <repo-folder>/qianchuan-ad-creative-workflow ~/.codex/skills/
```

If the repository root is already the skill folder:

```bash
git clone <repo-url> ~/.codex/skills/qianchuan-ad-creative-workflow
```

## Configure Keys

Copy:

```text
.env.example
```

to:

```text
.env
```

Then fill keys as needed. Do not commit `.env`.

Minimum configurations:

| Use case | Required keys |
|---|---|
| Planning only | None |
| Local material + MiniMax voice | `MINIMAX_API_KEY` |
| Network material search | `PEXELS_API_KEY`, `PIXABAY_API_KEY`; `COVERR_API_KEY` optional |
| Full-auto draft with network material and MiniMax | `PEXELS_API_KEY`, `PIXABAY_API_KEY`, `MINIMAX_API_KEY`; optional `COVERR_API_KEY`, `MINIMAX_GROUP_ID` |

Some MiniMax accounts require `MINIMAX_GROUP_ID`; if the API rejects a request without it, fill that value too.

## Verify Installation

From the skill folder:

```bash
python3 scripts/run_workflow.py --check
```

Expected result: a JSON status report showing available scripts and which keys are present or missing.

## Start In Chat

Tell the agent:

```text
使用 qianchuan-ad-creative-workflow，帮我做一个千川商品卡成交素材。
```

The agent should send the intake form from `references/prompt-starters.md`.

