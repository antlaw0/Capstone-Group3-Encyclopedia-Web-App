from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import os
import models as dbHandler

def sendPasswordEmail(receiverEmail):
	sender = "wintrteam@gmail.com"
	sender_password = "Capstone2905"#os.environ.get('WINTR_EMAIL_PASSWORD')
	receiver = receiverEmail
	username=dbHandler.getUsername(receiver)
	password=dbHandler.getPassword(receiver)
	
	# Create message container
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Wintr Password Reset"
	msg['From'] = sender
	msg['To'] = receiver

	# Create the body of the message (a plain-text and an HTML version).
	text = "Hello "+username+"\nThis is an email from the Wintr team to remind you that your password for Wintr is: \n"+password+"\n Thank you for using Wintr! \n sincerely, \n the Wintr team"
	html = """\
	<html>
	<head></head>
	<body>
		<p>
		Hello {username}<br>
		This is an email from the Wintr team reminding you of your password. Your Wintr password is:  <br>
		<br>
		{password}
		<br>
		<br>
		Thanks,<br>
		Wintr team
		</p>
	</body>
	</html>
	""".format(username=username, password=password)

	plain_text_message = MIMEText(text, 'plain')
	html_message = MIMEText(html, 'html')

	msg.attach(plain_text_message)
	msg.attach(html_message)
	
	# Send the message via the gmail server. Update as needed
	s = SMTP('smtp.gmail.com:587')
	s.starttls()
	s.login(sender, sender_password)
	s.sendmail(sender, receiver, msg.as_string())
	s.quit()

