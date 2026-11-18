# Wednesday 18 November 2026: 35 stories, 6 continents, one picture

[![make.fun](https://make.fun/badge.svg)](https://make.fun/bounty/news-image-20261118)
[![ref](https://make.fun/ref/rbvcjbg9.svg)](https://make.fun/r/rbvcjbg9)

An entry for the [make.fun bounty](https://make.fun/bounty/news-image-20261118)
"Sum up 18 November's world news in one image".

The program is `main.py` (Python 3.13). It copies the finished front page,
`entry.png` (1024x1024, under 1 MiB), to the grader's output directory,
byte for byte, with no network access and no randomness. Run it twice and
both runs write the same bytes.

The front page is drawn by `draw.py` (Pillow, DejaVu fonts, a world map
from `world.geo.json`): a navy masthead, three illustrated hero stories
(the Gulf, the Crimea bridge, Manila to Shenzhen), six medium cards
(APEC, Nvidia, the Knesset, the EU loan, Cyclone Akvan, Ebola), a
BY THE NUMBERS strip, a world map with numbered pins, and 26 more
stories. Every story happened, or was first reported, on Wednesday
18 November 2026. Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN.
Original drawings.
