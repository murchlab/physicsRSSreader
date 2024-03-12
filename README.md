# PhysicsRSSreader
Python based RSS reader for quantum physics.

# Requirements
python 2.7

# Configuration
- Edit `recipients.py` to include a list of email addresses.
- Edit the function `sendSummaryEmails` in `functionDefs.py` with a sender email account.
- (Optional) Edit `keywords.py` to include a list of keywords and authors.
- (Optional) Edit `feedURLsAndNames` in `physicsRSSreaderMain.py` to include a list of RSS sources.
- (Optional) Use the crontab service on a Linux server to host the script. Check out `physicsRSScronJob.txt` for an example configured in a anaconda env.

# Get started
Use python 2.7 to run

`python physicsRSSreaderMain.py`