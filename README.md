# Email Spam Classifier

A beginner rule-based email spam classifier built in Python.

## How it works
- Scans emails for spam keywords (free, winner, urgent, etc.)
- Subject line is weighted 2x more than the body
- Scores above 6.0 are flagged as SPAM

## Run it
```bash
python spam_classifier.py
```

## Tech
- Python 3
- No external libraries required
