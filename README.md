I wrote an automation script for the company where I work. We wanted to implement some kind of auto-reply referral code system, where users fill out a form and receive a unique referral code in a personalized email.

In terms of design, I decided that the CSV would be the "anchor" of the program from which all other actions would be determined, and where the most important data would reside. 
This was mostly because I needed a way to pick out externally generated referral codes that had already been initialized in our system and link them to a user via the email address they had entered. 
Naturally, I decided that this 'link' would be the indexes for each row of the CSV. The CSV also had the benefit of being easily readable by other non-programmers in the company, 
so those who want to quickly look at a neatly formatted list and see which client has which referral code, or even just get a general idea of how the referral program has been doing, can do so with expediently.

To paint a clearer picture of the flow of this whole thing, here's how it goes:

A client submits a simple form on our website, requesting a referral code. The form includes 3 fields: First Name, Last Name, and Email.
The relevant email address receives an email with a standardized header indicating that it is a referral code request email containing the user's submitted information.
Whenever the script runs, that email inbox is scraped for all emails with the standardized header
The data submitted email addresses are then compiled into a list, and checked against those already in the CSV.
If the email is already present in the CSV, the loop skips to its next iteration (email), printing to the console that the email was already found in the CSV.
If the email is not already in the CSV (new), Client() objects are created, storing the other data from the current email. (Client() objects are just used to store client data as attributes (client.name, client.email, client.code, etc))
The new email is then entered into the CSV, and a Client.code attribute is defined by the value of the 'Codes' column at the current index.
The relevant code is then sent to the email address the user initially entered in a well-formatted, personalized email.
After emails are sent, the matching cell under the 'email sent' column is given the value 'Yes' to ensure clients are not spammed with emails every time the script runs.
I am quite happy with my design of this script. In terms of logic / workflow I think it makes sense, and does a good job of maintaining the data integrity of the CSV every time the script is run (~every 5 minutes or so). 
I will admit the code is kind of messy to look at and parse, but I've only been learning for a few months, so I'm just happy it works as intended. I will be more mindful or writing cleaner code in the future, though.

I also obviously edited the code to remove credentials.
