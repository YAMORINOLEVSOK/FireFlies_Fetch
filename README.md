fireflies-bulk-download

Bulk‑download every Fireflies.ai transcript you own, as clean speaker‑by‑speaker text files, with a single Python command.

✨ Features

What it does

Why it matters

🔄 Paginates through all your meetings via Fireflies’ public GraphQL API

No more clicking “Download” one meeting at a time

🗣  Pulls the full sentence list (speaker‑labelled)

Gives you raw, analysis‑ready text—not the summary page HTML

💾 Saves each file as <title>_<id>.txt in an output/ folder

Easy to sort, grep, or ingest into ChatGPT & LLM pipelines

♻︎ Skips files it’s already downloaded

Safe to rerun any time—you’ll only fetch new stuff

⚠️  Gracefully skips meetings with no transcript data (e.g. still processing)

Keeps the run going, prints a warning, moves on

🛠  Just one dependency: requests

Works in any Python 3.8 + environment, including Replit & Codespaces

🖥  Requirements

Python 3.8+ (install from https://python.org or via Homebrew on macOS: brew install python@3)

A Fireflies.ai API token (Pro/Business plan or higher)

Heads‑up: Free plans don’t expose the API token menu. You can copy the token cookie instead, but the official token is easier.

🚀 Quick‑start

# 1  Grab the repo
$ git clone https://github.com/your‑username/fireflies‑bulk‑download.git
$ cd fireflies‑bulk‑download

# 2  (Optional) keep deps tidy with a venv
$ python3 -m venv venv && source venv/bin/activate

# 3  Install the single dependency
$ pip install requests

# 4  Export your Fireflies token (replace with your own)
$ export FIREFLIES_TOKEN="xxxxxxxx‑xxxx‑xxxx‑xxxx‑xxxxxxxxxxxx"

# 5  Run it
$ python3 fireflies_bulk_download.py

You’ll see lines like:

⬇︎  saved Customer Demo - 2024‑05‑01_a1b2c3d4.txt
✔︎  Kickoff Call - 2024‑04‑18_e5f6g7h8.txt already exists; skipping
⚠️  Weekly Sync - still processing; skipping

Finished files live in output/.

🔑 Obtaining your Fireflies API token

Log in at https://app.fireflies.ai.

Click Settings › Integrations.

At the bottom, open Developer / API and hit Generate Token.

Copy the long UUID string and export it as FIREFLIES_TOKEN.

(If you don’t see “Developer / API”, upgrade your plan or copy the token cookie via DevTools > Application > Cookies.)

🛠  Script options & tweaks

What

How

Change the page size

Edit PAGE_SIZE at the top (max = 50)

Throttle API calls

Adjust the time.sleep(0.2) line to be nicer or faster

Filter by date range

Replace the LIST_QUERY with the meetings query and pass startDate / endDate vars

Different output format

Convert text to JSON/CSV before fn.write_text()

Code is fully commented—feel free to hack away.

🆘 Troubleshooting

Symptom

Likely cause

Fix

RuntimeError: Unauthorized

Bad / expired token

Regenerate token, export FIREFLIES_TOKEN=...

KeyError: 'sentences'

Your plan returns a different field (e.g. segments)

Swap the inner GraphQL query accordingly

Script ends instantly, no output

No meetings in this workspace

Switch workspace in Fireflies or use the right account

Downloads HTML not text

You cloned an old commit – update to latest script

git pull

🤝 Contributing

Pull requests are welcome! Please open an issue first if you plan a large change so we can discuss.

📄 License

MIT

🙏 Acknowledgements

Original bulk‑export idea & first script by Leslie Barry

Tweaked & expanded by the Human Race team to handle speaker diarization, retries, and workspace‑safe reruns.

Happy exporting! 🎉
