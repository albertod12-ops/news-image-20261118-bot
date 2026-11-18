# news-image-20261118-bot

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/albertod12-ops/news-image-20261118-bot/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/albertod12-ops/news-image-20261118-bot/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

Wednesday 18 November 2026: 35 stories, 6 continents, one picture — an entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261118) "Sum up 18 November's world news in one image".

The program is `main.py` (Python 3.13). It copies the finished front page, `entry.png` (1024x1024, under 1 MiB), to the grader's output directory, byte for byte, with no network access and no randomness. Run it twice and both runs write the same bytes.

The front page is built by `draw.py` (Pillow, DejaVu fonts, a world map from `world.geo.json`): a navy masthead, three hero stories with photorealistic illustrations (the Gulf, the Crimea bridge, Manila to Shenzhen), six medium cards with photos (APEC, Nvidia, the Knesset, the EU loan, Cyclone Akvan, Ebola), a BY THE NUMBERS strip, a world map with numbered pins, and 26 more stories. Every story happened, or was first reported, on Wednesday 18 November 2026. Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original illustrations.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=rbvcjbg9&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
