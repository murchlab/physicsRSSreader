# PhysicsRSSreader
Python based RSS reader for quantum physics. Once a day it checks journal and arXiv feeds and emails a digest of
papers by authors you follow ("probably of interest") and papers matching your keywords ("possibly of interest").

# Requirements
Python 3.8+ and `feedparser` (`pip install feedparser`)

# Configuration
- `recipients.py`: list of email addresses that get the digest.
- `email.txt`: the email account that sends it. Line 1 is the Gmail address and line 2 is its
  [app password](https://myaccount.google.com/apppasswords), not the normal password. This file is git-ignored;
  never commit it. Lines starting with `#` are ignored. To use a mail server other than Gmail, add
  `host = ...` / `port = ...` lines, or use `smtpSettings.ini` (see `smtpSettings.example.ini`).
- `keywords.py`: authors and keywords to match.
- `feedURLsAndNames` in `physicsRSSreaderMain.py`: the RSS feeds. If a feed stops working, the digest ends with a
  warning naming it.
- `latestRunDateTime`: date of the last run (YYYYMMDD). Papers since this date are included. Set it to yesterday
  before the first run, or the first digest will contain everything currently in every feed.

# Running
Normal daily run (emails everyone in `recipients.py`, updates `latestRunDateTime`):

`python physicsRSSreaderMain.py`

Trying it out (these never touch `latestRunDateTime`; by default they cover the last 3 days):

- `python physicsRSSreaderMain.py --preview digest_preview.eml` writes the email to a file instead of sending it.
- `python physicsRSSreaderMain.py --test you@example.edu` sends the digest only to you.
- Add `--since YYYYMMDD` to either to choose the start date.

# Scheduling (Linux cron)
See `physicsRSScronJob.txt` for an example that activates a conda env, `cd`s into this folder and runs the script
every morning. Copy `email.txt` to the server next to the script and make it private (`chmod 600 email.txt`).
