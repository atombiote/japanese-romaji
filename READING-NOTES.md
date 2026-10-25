# Reading notes

These notes explain selected readings used in v0.2.0 and retained in v0.3.0-beta.1. They are not a claim of independent human review.

## Selected dictionary checks

- 原木: genboku, from げんぼく. [Digital Daijisen entry](https://kotobank.jp/word/原木-61096).
- 板材: itazai, from いたざい. [Digital Daijisen entry](https://kotobank.jp/word/板材-432942).
- 樹皮: juhi, from じゅひ. [Digital Daijisen entry](https://kotobank.jp/word/樹皮-78149).
- 剥ぐ: hagu; the past form 剥いだ is rendered haida. [Nihon Kokugo Daijiten entry](https://kotobank.jp/word/剥ぐ-2073889).
- 竹細工: takezaiku, from たけざいく. [Digital Daijisen entry](https://kotobank.jp/word/竹細工-560025).
- 養蜂箱: yōhōbako, from ようほうばこ. [Tangorin dictionary entry](https://tangorin.com/words/養蜂箱).
- 感圧板: kan'atsuban. A publisher's Minecraft guide supplies the kana かんあつばん. [Shinyusha guide sample](https://www.shinyusha.co.jp/wp-content/uploads/2025/12/P114-117_23%E5%8D%A0%E3%81%84%E3%81%AE%E9%A4%A8.pdf).

## Conventions

Modified-Hepburn-style readings use macrons for long vowels where appropriate, retain n before b/m/p (kanban, konposutā), and use an apostrophe where n precedes a vowel (kan'atsuban). Familiar consecutive vowels such as ii in tamashii are retained. Word spacing is a readability choice; it is not a syllable or timing breakdown.

The particle を is rendered o. 剥いだ is haida, not hagu or hagashita. 歪んだ is rendered yuganda. 苗木 is naegi; 幹 is miki; 菌糸 is kinshi. Family names and recurring block terms are applied consistently.

COVERAGE.md links the complete English/Japanese/romaji lists under coverage/. The Japanese spellings are copied unchanged only for the selected overrides. The installed Japanese language asset also contains newer-version keys; selected entries are constrained to names actually present in the verified 1.21.1 client.


## Full beta generation

The expansion uses [SudachiPy](https://github.com/WorksApplications/sudachi.rs) and [SudachiDict](https://github.com/WorksApplications/SudachiDict) to obtain context-sensitive kana readings, followed by a project kana-to-Hepburn converter. It applies word/phrase corrections from data/reading-overrides.json and retains the prior 264 readings exactly.

Corrections include gold as kin in gold equipment, shinsōgan for 深層岩, shōrai for 召雷, kaji for 鍛冶, chikufū for 蓄風, and common food names. These decisions improve the first dictionary pass but are not independent linguistic approval. Space placement is approximate, and dictionary-selected readings can still be wrong for a particular sentence or invented game term.

The original Japanese text is never replaced by a new translation. Placeholder-bearing messages are annotated in fixed-text chunks so runtime arguments are not duplicated. Mixed Latin text and Arabic numbers remain recognizable letters/digits.
