# Recipients for the physics RSS digest are read from recipients.txt (git-ignored, so addresses stay private).
# recipients.txt: one email address per line; blank lines and lines starting with # are ignored.
import os

RECIPIENTS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recipients.txt')


def loadRecipients():
    if not os.path.exists(RECIPIENTS_FILE):
        raise RuntimeError('No recipients.txt found. Create it next to physicsRSSreaderMain.py with one email '
                           'address per line.')
    with open(RECIPIENTS_FILE, encoding='utf-8-sig') as f:
        addresses = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    if not addresses:
        raise RuntimeError('recipients.txt has no email addresses in it.')
    return addresses
