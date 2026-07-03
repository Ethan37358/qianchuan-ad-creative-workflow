# Setup

Use this when the user wants to run the Qianchuan workflow on a new computer or asks where to put API keys.

## Required Configuration

Copy `.env.example` from the skill folder to the project folder as `.env`, then fill the values:

```text
PEXELS_API_KEY=
PIXABAY_API_KEY=
COVERR_API_KEY=
MINIMAX_API_KEY=
MINIMAX_GROUP_ID=
MINIMAX_TTS_MODEL=speech-02-hd
MINIMAX_TTS_VOICE_ID=Chinese (Mandarin)_Warm_Girl
```

Only Pexels/Pixabay are required for those material providers. Coverr is optional until the user's account/API access is confirmed. MiniMax requires `MINIMAX_API_KEY`; some accounts also require `MINIMAX_GROUP_ID`.

## Env Loading Behavior

Bundled scripts automatically search for `.env` in:

1. The current project folder
2. Parent folders near the current project
3. The skill folder
4. The skill `config/` folder

The user can also pass `--env /path/to/.env`.

Existing shell environment variables override values from `.env`.

## First Test Commands

Material collector dry run:

```bash
python3 scripts/material_collector.py --storyboard /path/to/storyboard.json --out /tmp/candidates.json
```

MiniMax dry run:

```bash
python3 scripts/minimax_tts.py --text /path/to/voiceover.txt --out /tmp/voice.mp3 --dry-run
```

Unified runner check:

```bash
python3 scripts/run_workflow.py --check
```

If keys are missing, scripts should report exactly which keys are missing.

## Portability Rule

Do not hard-code API keys into scripts, generated documents, or chat responses. Keep real secrets only in `.env` or system environment variables.
