# Validation - v0.3.0-beta.1

Checked 25 October 2026.

The installed Java 1.21.1 client supplied 6,881 English translation keys. The installed Japanese asset supplied the original text. The client JAR SHA-1 was previously checked against the official local version metadata: 30c73b1c5da787909b2f73340419fdf13b9def88. The Japanese asset SHA-1 is 93054df00419a33c4336b14c05c8896177556621.

## Passed checks

- The installable ZIP contains exactly pack.mcmeta, pack.png, NOTICE.txt, LICENSE.txt and assets/minecraft/lang/ja_jp.json with portable paths and no enclosing folder.
- ZIP integrity and UTF-8/JSON decoding pass; duplicate JSON keys are rejected.
- Resource-pack format is 34, matching the verified 1.21.1 client.
- All 6,506 eligible Japanese entries are annotated, with no newer-version-only keys.
- Original text is recovered exactly for every entry by removing its recorded insertions. No original Japanese character or punctuation is changed.
- All 1,378 formatting placeholders, percent tokens, formatting codes, line breaks and URLs in annotated entries remain identical and in order.
- Added readings contain no unresolved Japanese script or unfinished transliteration markers.
- All 264 entries from v0.2.0 retain their exact values.
- All 6,881 input keys are accounted for: 6,506 annotated, 279 without Japanese script, three technical language-metadata keys, and 93 absent from the installed Japanese asset. Missing translations retain the game's English fallback.
- Packaged language bytes match the editable source and the release manifest's SHA-256.
- The shipped generator, using pinned dictionary tools and retained-reading data, reproduces the exact language file.
- The previous v0.1.0 and v0.2.0 ZIPs remain available for rollback.

ZIP size: 208,770 bytes.

ZIP SHA-256: 88b3b62b61e4f7b3138e8ed9804fe5a0ade7cfee8e7c0742be40b180b5967d43

## Practical limits

These checks establish coverage and file/formatting integrity, not linguistic correctness. Most new readings are dictionary-generated with project-specific corrections. Common gameplay vocabulary was inspected, but no independent human Japanese proofreading has been performed.

The full pack has not been launched in Minecraft by the assistant. Tooltip width, option/button clipping, language switching and interaction with the user's NeoForge setup still require an in-game check. Narrator output includes added Latin text. No runtime code, dictionaries, game textures, sounds or non-Japanese language files are bundled. The only image is the publisher's original artwork, converted to PNG for the pack icon.

The public beta was prepared after the publisher authorized GitHub release. The original artwork and matching pack icon were added without changing the language values.
