# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/rismzz/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/rismzz/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A dense broadsheet that sums up Tuesday 24 November 2026 in a single
1024×1024 image: 35 headline stories, every one first reported that day.
Lead: Anthropic launches Claude Ship, an AI that reviews, fixes and
approves code. Also inside: Schumer vows a probe into possible wrongdoing
behind Nvidia's reinstatement of Huang, an appeals court gives Trump a
path to erasing his hush-money conviction, the US moves to blacklist AI
firm Megaspeed, Denmark's top court backs the hardline "ghetto law", a
lion is on the loose near Istanbul, and Gukesh defends his world chess
crown against Sindarov in Geneva — plus a first-reported UTC timeline
strip, a markets ticker with Monday's closes, and a visible DATE CHECK
line.

Early edition: built at 00:40 UTC from stories verified so far. A
full-day rebuild will replace this edition before entries close.

## Run it

```sh
python3 render_frontpage.py   # rebuild entry.png (1024x1024, < 1 MiB)
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`render_frontpage.py` draws the poster with Pillow (DejaVu fonts, no
network) and writes `entry.png`. `main.py` is the entrypoint: it verifies
the PNG (magic bytes, IHDR chunk, 1024×1024, at most 1 MiB) and copies it,
with a sha256 check, to `$MAKEFUN_OUTPUT_DIR/entry.png` (default
`/output`). Deterministic: two runs write identical bytes.

## License

MIT — see [LICENSE](LICENSE).

---
Built for the [make.fun bounty](https://make.fun/bounty/news-image-20261124?ref=aa4mcy45) — $100 USDC, 50 places.
Play make.fun with my referral: https://make.fun/?ref=aa4mcy45
