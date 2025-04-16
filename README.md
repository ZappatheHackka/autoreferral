# Fully Automated Referral Code Mailbot 📬

A Python automation script used in production to:
- Parse new referral requests from an email inbox (via IMAP)
- Store new entries in a CSV (deduplicated)
- Send personalized, unique referral codes via SendGrid (HTML email)
- Log and track code delivery status

## Tech Stack

- Python
- IMAPClient
- pandas
- SendGrid API
- xlsx / CSV for lightweight persistence

## Why I Built It

Built to streamline the referral onboarding process at my company, completely replacing a multi-step manual workflow with an instantaneous, fully automated script.

## How to Use

- Fill in your credentials
- Configure IMAPClient to scrape emails based on your specifics
- Set up a CSV file with the correct headers (`Client Emails`, `Code Sent`, `Codes`), or modify the script to work with your specific headers
- Ensure the 'Codes' column is populated with your specific codes
- Run the script to automatically send referral codes to new clients

