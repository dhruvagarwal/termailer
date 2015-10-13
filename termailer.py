#!/usr/bin/python2
from Tkinter import Tk
from getpass import getpass
from tempfile import NamedTemporaryFile
from tkFileDialog import askopenfilename
import os
import re
import smtplib
import subprocess

from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate

from termailer.exceptions import IncorrectEmailException
from termailer.settings import SMTP_CLIENT_FOR_DOMAIN


def get_domain(email_address):
    regex = r"\w(?:\.|\_|\w)*@(\w+)\.\w(?:\w|\.|\_)*"
    if re.match(regex, email_address):
        domain_name = re.split(regex, email_address)[1]
        return domain_name

    raise IncorrectEmailException


def check_domain(domain):
    """Check suuport for given domain."""
    if domain in SMTP_CLIENT_FOR_DOMAIN:
        return True

    error_message = "Unknown domain name - '" + domain + "'.\n"
    error_message += """Following email providers are supported-:
                    {domain_list}""".format(domain_list='\n'.join([key for
                                                key in SMTP_CLIENT_FOR_DOMAIN]))

    raise Exception(error_message)


def get_recipients():
    print 'Enter list of recipents separated by comma(,)'
    recipents = map(lambda x: x.strip(), raw_input().strip().split(','))
    return recipents


def get_body():
    body = ""

    # Create a temporary file
    body_buffer_file = NamedTemporaryFile(delete=False)
    body_buffer_file_path = body_buffer_file.name
    body_buffer_file.close()

    # Set the default editor
    editor = 'nano'
    if os.name is 'nt':
        editor = 'notepad'

    raw_input('Press Enter to start writing the body of the mail')
    try:
        subprocess.call([editor, body_buffer_file_path])
    except OSError:
        # No suitable text editor found
        # Let the user edit the buffer file himself
        print "Enter the mail body in the file located at '" + body_buffer_file_path + "'"
        raw_input("Press Enter when done!")

    body_buffer_file = open(body_buffer_file_path)
    body = body_buffer_file.read()
    body_buffer_file.close()
    try:
        os.remove(body_buffer_file_path)
    except:
        # Unable to remove the temporary file
        # Stop the exception from propogating further,
        # since removing it is not essential to the working of the program
        pass

    return body


def get_attachments():
    attachments = []

    print 'Select the attachment files.\n(Press cancel to finish!)'
    Tk().withdraw()
    while True:
        attachment = askopenfilename()
        if not attachment:
            break
        attachments.append(attachment)

    return attachments


def send_mail(email, email_provider_addr, password, recipients, subject, body, attachments):
    if not recipients:
        raise Exception("Please add atleast one recipient!")

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = COMMASPACE.join(recipients)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    print "Attaching body ..."
    msg.attach(MIMEText(body))

    for attachment in attachments:
        print "Attaching - '" + attachment + "' ..."
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(attachment, "rb").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(attachment))
        msg.attach(part)

    print 'Establishing connection ...'
    server = smtplib.SMTP(email_provider_addr, 587)
    # Identify ourselves to the SMTP client
    server.ehlo()
    # If we can encrypt this session, do it
    if server.has_extn('STARTTLS'):
        # Secure our email with TLS encryption
        server.starttls()
        # Re-identify ourselves over the TLS connection
        server.ehlo()

    print 'Authorizing ...'
    server.login(email, password)

    print 'Sending mail ...'
    server.sendmail(email, recipients, msg.as_string())

    print 'Closing connection ...'
    server.quit()


def main():
    try:
        email = raw_input('Email address: ')
        email_domain = get_domain(email)
        check_domain(email_domain)
        password = getpass()
        recipients = get_recipients()
        subject = raw_input('Subject: ')
        body = get_body()
        attachments = get_attachments()

        send_mail(email, SMTP_CLIENT_FOR_DOMAIN[email_domain],
                password, recipients, subject, body, attachments)
        print 'Mail sent!!'

    except BaseException as exception:
        error_message = exception.message
        if not error_message:
            error_message = str(exception)
        print "Error : {0}".format(error_message)


if __name__ == '__main__':
    main()
