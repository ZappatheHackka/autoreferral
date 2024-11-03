import email
import pandas as pd
from imapclient import IMAPClient
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, MimeType


class Client:
    def __init__(self, email, name):
        self.email = email
        self.name = name
        self.code = 0


MAIL_USER = 'your_email'
MAIL_PASS = 'your_pass'
MAIL_LINK = 'site'
PORT = 'port'

# List of Client objects that have already been added
list_of_contacts = []
df = pd.read_csv('BUCKets_Referral_Codes.csv')
df['Client Emails'] = df['Client Emails'].astype(str)
# Logging into email address & server with Imapclient
server = IMAPClient(host=MAIL_LINK, port=PORT, use_uid=True)
server.login(username=MAIL_USER, password=MAIL_PASS)
data = server.select_folder(folder='Inbox')

print('%d messages in INBOX' % data[b'EXISTS'])


def user_in_list():
    emails_in_db = df['Client Emails'].tolist()
    return [email.strip().lower() for email in emails_in_db if email != 'nan']


def fetch_info():
    messages = server.search(criteria=['Subject', 'NEW REFERRAL REQUEST'])
    for message in messages:
        msg_dt = server.fetch([message], ['RFC822'])
        msg = email.message_from_bytes(msg_dt[message][b'RFC822'])
        if msg.get_content_type() == 'text/plain':
            msg_body = msg.get_payload(decode=True).decode(msg.get_content_charset())
            msg_contents = msg_body.split('\n')
            msg_email = msg_contents[2][7:].rstrip().lower()

            # Check if email is already in the CSV
            if msg_email in user_in_list():
                print(f"Email {msg_email} already in CSV - skipping.")
                continue

            msg_name = msg_contents[0][6:].rstrip()
            obj = Client(name=msg_name, email=msg_email)
            list_of_contacts.append(obj)
            print(f'Client object created of contact info for {msg_email}--added to list_of_contacts')


fetch_info()

# Looping through collected data and adding each unique email address to 'BUCKets_Referral_Codes.csv
existing_emails = user_in_list()
for contact in list_of_contacts:
    if contact.email.lower() not in existing_emails:
        # Find the first empty row
        empty_row = df[df['Client Emails'] == 'nan'].index[0]
        df.at[empty_row, 'Client Emails'] = contact.email
        df.at[empty_row, 'Code Sent'] = 'No'  # Ensure new entries are marked as not sent
        print(f"Adding {contact.email} to the CSV.")
    else:
        print(f"Email {contact.email} already in CSV - skipping.")

df = df.dropna(subset=['Client Emails'])
df.to_csv('BUCKets_Referral_Codes.csv', index=False)


def clients_to_email():
    list_of_clients = []
    for index, row in df.iterrows():
        if row['Code Sent'] == 'No' and row['Client Emails'] != 'nan':
            client_email = row['Client Emails']
            client_name = row['Client Emails'].split('@')[0]  # Use email as name if no name is available
            client = Client(email=client_email, name=client_name)
            client.code = row['Codes']
            list_of_clients.append(client)
    return list_of_clients


def mailbot(clients):
    if clients:
        for client in clients:
            # Create SendGrid mail object
            from_email = Email("Referral Program <" + MAIL_USER + ">")
            to_email = To(client.email)
            subject = "Your ___ Referral Code"

            # Use HTML content to ensure proper formatting
            html_content = f"""
            <html>
            <body style=color:black;>
            <p>Hello {client.name},</p>
            <p>Thank you for joining the _____ Referral Program!</p>
            <br>
            <p>Your personal referral code is: <strong>{client.code}</strong></p>
            <br>
            <p>Share this code with new clients to earn rewards. The more you share, the more you earn!</p>
            <p>If you have any questions, please reply to this email.</p>
            <br>
            <p>Best regards,</p>
            <p>The ______ Team</p>
            <br>
            <hr>
            <p><em>This is an automated message.</em></p>
            </body>
            </html>
            """

            content = Content(MimeType.html, html_content)

            mail = Mail(from_email, to_email, subject, content)
            mail.reply_to = Email(MAIL_USER)

            try:
                sg = SendGridAPIClient('your_apikey')
                response = sg.send(mail)
                print(f"Sent email to {client.email}. Status code: {response.status_code}")

                if response.status_code == 202:
                    df.loc[df['Client Emails'] == client.email, 'Code Sent'] = 'Yes'
                    df.to_csv('BUCKets_Referral_Codes.csv', index=False)
                    print(f"Updated 'Code Sent' status for {client.email}.")
                else:
                    print(f"Failed to send email to {client.email}. Status code: {response.status_code}")

            except Exception as e:
                print(f"Error sending email to {client.email}: {str(e)}")

    else:
        print("All clients have been sent their associated referral codes.")


mailbot(clients_to_email())