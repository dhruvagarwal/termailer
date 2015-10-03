import os
import smtplib
from getpass import getpass
from tempfile import NamedTemporaryFile
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

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
    
    raw_input('Press Enter to start writing the body of the mail')
    os.system('nano ' + body_buffer_file_path)
    body_buffer_file = open(body_buffer_file_path)
    body = body_buffer_file.read()
    body_buffer_file.close()
    try:
        os.remove(body_buffer_file_path)
    except:
        # Unable to remove the temporary file
        pass
    
    return body


def get_attachments():
    attachments = []
    
    print 'Enter the paths of the attachment files, one per line-:\n(Enter a blank line to finish!)'
    while True:
        attachment = raw_input()
        if not attachment:
            break
        attachments.append(attachment)
    
    return attachments


def send_mail(username, password, recipients, subject, body, attachments):
    if not recipients:
        raise Exception("Please add atleast one recipient!")
    
    msg = MIMEMultipart()
    msg['From'] = username
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
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Identify ourselves to the SMTP Gmail client
    server.ehlo()
    # If we can encrypt this session, do it
    if server.has_extn('STARTTLS'):
        # Secure our email with TLS encryption
        server.starttls()
        # Re-identify ourselves over the TLS connection
        server.ehlo()
    
    print 'Authorizing ...'
    server.login(username, password)
    
    print 'Sending mail ...'
    server.sendmail(username, recipients, msg.as_string())
    
    print 'Closing connection ...'
    server.quit()


def main():
    try:
        username = raw_input('Username: ')
        password = getpass()
        recipients = get_recipients()
        subject = raw_input('Subject: ')
        body = get_body()
        attachments = get_attachments()
              
        send_mail(username, password, recipients, subject, body, attachments)
        print 'Mail sent!!'
    except BaseException as exception:
        error_message = exception.message
        if not error_message:
            error_message = str(exception)
        print "Error : {0}".format(error_message)


if __name__ == '__main__':
    main()
