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

1. **Set your credentials**  
   Add your email, SendGrid key, and other secrets to environment variables or a `.env` file.

2. **Configure email scraping**  
   Update the `IMAPClient` setup to target your inbox and match the right email content.

3. **Prepare your CSV**  
   Ensure the file includes the following headers:
   - `Client Emails`
   - `Code Sent` (e.g. TRUE/FALSE)
   - `Codes` (list of unique referral codes)

4. **Run the script**  
   It will:
   - Check for new clients
   - Send referral codes
   - Update the CSV accordingly

