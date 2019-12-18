################
# Dependencies #
################

from flask import Flask, escape, request  # pip install flask
from html2text import HTML2Text  # pip install html2text
from validate_email import validate_email  # pip install validate_email
from sendgrid import SendGridAPIClient  # pip install sendgrid
from sendgrid.helpers.mail import Mail

import copy
import requests
import os

####################
# Global Variables #
####################

app = Flask(__name__)
html2text_converter = HTML2Text()

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
EMAIL_PROVIDER = os.environ.get('EMAIL_PROVIDER')
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_DOMAIN_NAME = os.environ.get('MAILGUN_DOMAIN_NAME')

###########
# Routing #
###########

@app.route('/')
def default_route():
    pass

@app.route('/email', methods=['POST'])
def email_sender():
    """
        Main routing function: Given a POST request with formatted email data, verifies the email information and then sends it.
    """

    form = request.form.to_dict()
    email_obj = Email(form)

    is_str_values = email_obj.text_validation()
    if not is_str_values:
        return error_formatting()

    if type(email_obj.to_addr) == list:  # When there are more than 1 email recipients.
        result = [validate_email(addr) for addr in email_obj.to_addr]
        is_addr1 = all(result)
    else:
        is_addr1 = validate_email(email_obj.to_addr)

    is_addr2 = validate_email(email_obj.from_addr)

    if not (is_addr1 and is_addr2):  # If at least one of the email addresses within the Email fields is incorrectly formatted.
        return bad_email_destinations()

    email_obj.body_conversion()
    answer = email_obj.to_dict()
    email_obj.send_email()
    return "Email was sent successfully."

##########
# Errors #
##########

def error_formatting():
    """
        Occurs if there was an invalid field value within the email data (Email.text_validation returned False.)
    """
    return "There was a problem with the email format sent to the server - please verify the values are proper and valid."

def error_recipient():
    """
        Occurs if there was an invalid field value within the email data (validate_email(email addr) returned False.)
    """
    return "There was an invalid or non-existing email address marked as an email recipient. Please try again."

###########
# Classes #
###########

class Email:
    #  An Email object stores the information necessary to craft an email - the sender's information, the recipient(s) information, and the email subject and body.

    def __init__(self, email_dict):
        self.to_addr = email_dict.get('to')
        self.to_name = email_dict.get('to_name')
        self.from_addr = email_dict.get('from')
        self.from_name = email_dict.get('from_name')
        self.subject = email_dict.get('subject')
        self.body = email_dict.get('body')


    def text_validation(self):
        """
            Verifies that the fields within the email are strings.
            A future addition may be allowing for JSON values that aren't strings.
        """
        for field in [self.to_addr, self.to_name, self.from_addr, self.from_name, self.subject, self.body]:
            field_type = type(field)

            if field == self.to_name or field == self.to_addr:
                if field_type not in [str, list]:
                    return False

                if field_type == list:
                    for addr in field:
                        if type(addr) != str:
                            return False

            elif field_type != str:
                return False

        return True

    def body_conversion(self):
        """
            Converts the body of the email into Markdown plaintext through HTML2Text.
            Future implementation may involve using BeautifulSoup to parse the body instead.
        """
        plaintext = html2text_converter.handle(self.body)
        self.body = plaintext

    def to_dict(self):
        """
            Converts the Email object into a dictionary. We need to modify existing object.__dict__ because
            we can't use self.from as an attribute: 'from' is a Python keyword.
        """
        cur_dict = copy.deepcopy(self.__dict__)
        cur_dict['to'] = cur_dict.pop('to_addr')
        cur_dict['from'] = cur_dict.pop('from_addr')
        return cur_dict

    def send_email(self):
        """
            Tries to send an email to appropriate receiver, depending on environment variable EMAIL_PROVIDER.
        """
        if EMAIL_PROVIDER == "MAILGUN":
            requests.post(
                "https://api.mailgun.net/v3/%s/messages" % MAILGUN_DOMAIN_NAME,
                auth=("api", MAILGUN_API_KEY),
                data={"from": "%s <mailgun@%s>" % (self.from_name, MAILGUN_DOMAIN_NAME), 
                      "to": self.to_addr,
                      "subject": self.subject,
                      "text": self.body
                }
            )

        elif EMAIL_PROVIDER == "SENDGRID":
            message = Mail(
                from_email = self.from_addr,
                to_emails = self.to_addr,
                subject = self.subject,
                html_content = self.body
            )

            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)

            except Exception as e:
                print(e.message)

        else:
            print("Provider not found. Provider was %s." % EMAIL_PROVIDER)
