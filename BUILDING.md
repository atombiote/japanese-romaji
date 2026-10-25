# Building

## Package the current source

Run **./build.ps1** in PowerShell from this folder. It uses .NET ZIP support, validates the release's language hash and key list, and writes the ZIP specified in release.json. No Python packages are required for packaging.

## Regenerate readings

The generator uses Python 3.12 with **SudachiPy==0.6.10** and **SudachiDict-core==20250129**. Install requirements-build.txt in a local environment or a folder passed as --deps. These are build-time tools; none are bundled in the resource pack.

Supply your own local vanilla 1.21.1 en_us.json and installed ja_jp.json. From this project folder:

    python tools/generate.py --english PATH_TO_EN_US.json --japanese PATH_TO_JA_JP.json --deps PATH_TO_TOOLS --out BUILD_OUTPUT --retained data/retained-readings.json --overrides data/reading-overrides.json

The generator writes an intermediate language file, insertion audit, coverage and unknown-token reports. Inspect these and correct readings before promoting a pass. An empty unknown-token list does not prove pronunciation accuracy.

Promoting changes requires updating pack/assets/minecraft/lang/ja_jp.json, data/annotation-spans.json, coverage/exception reports and release.json together. Refresh the language SHA-256 in release.json after edits. The annotation-spans data records insertion positions and additions, permitting exact original-text recovery.

## Validate

    python tools/validate.py --root . --english PATH_TO_EN_US.json --japanese PATH_TO_JA_JP.json

The validator uses Python's standard library. It checks the ZIP layout, JSON, original-text recovery, formatting placeholders/codes/newlines/URLs, eligible-key coverage, retained entries and exceptions. Its current expected totals target v0.3.0-beta.1. File validation does not replace Japanese proofreading or an in-game layout test.
