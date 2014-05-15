import smtplib,os
from getpass import getpass
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

username = fromaddr = raw_input('Username: ')
password = getpass()

toaddrs  = raw_input('Enter list of recipents separated by a comma : ').split(',')

def mailscript(send_from,send_to,subject,text,files=[]):
	msg=MIMEMultipart()
	msg['From'] = send_from
	msg['To'] = COMMASPACE.join(send_to)
	msg['Date'] = formatdate(localtime=True)
	msg['Subject'] = subject

	msg.attach(MIMEText(text))
	try:
		for f in files:
			part = MIMEBase('application', "octet-stream")
			part.set_payload( open(f,"rb").read() )
			Encoders.encode_base64(part)
			part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
			msg.attach(part)
	        
	except:
		print 'There was some error in attaching the attachments.'
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg.as_string())
	server.quit()

def checkpath(p):
	comm="if [ -f "+p+" ];\nthen\necho '1'\nelse\necho '0'\nfi"
	return int(os.popen(comm).read())

def takea():
	l=[]
	y=raw_input('Do you want to attach something ? (y/n) ')
	while y=='y':
		p=raw_input('Enter complete file path of the attachment : ').strip()
		if checkpath(p):
			l.append(p)
		y=raw_input('Do you want to attach more ? (y/n) ')
	return l

subject=raw_input('Enter subject of the mail: ')
x=raw_input('Enter your Mail body (Press Enter to start):')
os.system('nano tempbody.txt')
text=open('tempbody.txt').read()
attachments=takea()
print 'Sending mail ...'
mailscript(fromaddr,toaddrs,subject,text,attachments)
os.system('rm tempbody.txt')
print 'Mail Sent to '+','.join(toaddrs)