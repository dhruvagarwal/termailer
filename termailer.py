#!/usr/bin/python2
import os
import subprocess
import smtplib
from Tkinter import Tk
from tkFileDialog import askopenfilename
from getpass import getpass
from tempfile import NamedTemporaryFile
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders


email_provider_address = {
'gmail':'smtp.gmail.com',
'outlook':'smtp-mail.outlook.com',
'hotmail':'smtp-mail.outlook.com',
'live':'smtp-mail.outlook.com',
'yahoo':'smtp.mail.yahoo.com',
'icloud':'smtp.mail.me.com',
'aol':'smtp.aol.com',
'yandex':'smtp.yandex.com',
'zoho':'smtp.zoho.com',
}


# Parse the domain part from an email address
def get_domain(email):

    i = len(email) - 1    
    while i >= 0 and email[i] != '@':
        i -= 1
    
    j = i + 1
    while j < len(email) and email[j] != '.':
        j += 1
    
    return email[i+1:j]

# Makes sure that the domain is supported
# Raises an exception if it isn't
def check_domain(domain):
    if not domain in email_provider_address:
        error_message = "Unknown domain name - '" + domain + "'.\n"
        error_message += "Following email providers are supported -:\n"
        for email_provider in email_provider_address:
            error_message += email_provider + "\n"
        raise Exception(error_message)


def get_recipients():
    recipients = []
    
    print 'Enter the list of recipients, one per line-:\n(Enter a blank line to finish!)'
    while True:
        recipient = raw_input()
        if not recipient:
            break
        recipients.append(recipient)
    
    return recipients


def get_body():
    body = ""
    
    # Create a temporary file
    body_buffer_file = NamedTemporaryFile(delete = False)
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
    msg['Date'] = formatdate(localtime = True)
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
              
        send_mail(email, email_provider_address[email_domain], password, recipients, subject, body, attachments)
        print 'Mail sent!!'
    except BaseException as exception:
        error_message = exception.message
        if not error_message:
            error_message = str(exception)
        print "Error : {0}".format(error_message)


if __name__ == '__main__':
    main()
