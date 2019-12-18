# Email Service

This is a conceptual version of a service-fault-tolerant email service that receives POST requests with email data and then sends the email accordingly to its intended recipients.

## How to Install
1) Install Python on your computer, if necessary.
2) Clone or download the repo to your computer.
3) Open the command line and navigate to the email service directory.
3) Run "pip (Python 2) or pip3 (Python 3) install -r requirements.txt" to get the dependencies.
4) Run "env FLASK_APP=email_service.py flask run" to begin running the email service.

You will need to set up accounts with Sendgrid and Mailgun in order to get API keys, which will enable the email service to send emails through these API services.

Finally, you'll need to set up environmental variables for the email service. You can either export each variable for the current session, or you can set up a .env file that exports the variables for you, which you would then run with "source .env".

The environmental variables, which are also denoted in email_service.py, are as follows:
- EMAIL_PROVIDER: when set to "MAILGUN" or "SENDGRID", it will use that API service to send the email.
- SENDGRID_API_KEY: obtained when setting up account with Sendgrid.
- MAILGUN_API_KEY: obtained when setting up account with Mailgun.
- MAILGUN_DOMAIN_NAME: obtained when setting up account with Mailgun.

After these environmental variables are setup properly, you can re-run Flask (step 4) to get a functional email service that receives POST requests!

## Implementation
In terms of language, I chose to work with Python, the language I'm very confident in working with. Requests is a common Python library used for working with HTTP requests. I've worked with AWS Chalice before, so I picked Flask because it's not only commonly used, but it's pretty similar to working with AWS Chalice. HTML2Text helped me convert any HTML-formatted email bodies to Markdown-formatted text, which some email services can use to format their emails. Lastly, validate_email helped me validate email addresses to make sure they were not only formatted properly, but also existing email addresses. Sendgrid and Mailgun are email API services that are easy to sign up with, so that's why I chose to use them - and having 2 of them makes the email service fault-tolerant because if 1 of them goes down, one only needs to modify their EMAIL_PROVIDER environmental variable and redeploy to quickly make the service functional again.

## Further Work
If I had more time to work on this project, there's a few things I probably would change. Some of these changes are laid out in email_service.py.

- Possibly using BeautifulSoup instead of HTML2Text for email body parsing and conversion. Although I really liked the convenience of HTML2Text, my experience was that the Markdown-formatted text was not consistent in output across Sendgrid and Mailgun, which would serve as a potential problem.
- Using Python PEP-8 formatting guidelines a bit more tightly - my lines could potentially be too long; line spacing might be off.
- Consider more errors with the program and test them - for example, I didn't get to test what would've happened if the subject was empty.
- Have more helpful client-side information or errors about what's going on with the server. All that happens is that the user either knows that their email failed for a given reason, or that it got sent.
