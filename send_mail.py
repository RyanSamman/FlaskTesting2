import smtplib
from email.mime.text import MIMEText

def send_mail(customer, dealer, rating, comments):
	port = 2525
	smtp_server = 'smtp.mailtrap.io'
	login = '1e8a442cc52bce' 
	password = '1a500fa6570f7d'

	message = (f"<h3>New Feedback Submission<h3>"
	+ "<ul>"
	+ f"<li>Customer: {customer}</li>"
	+ f"<li>Dealer: {dealer}</li>"
	+ f"<li>Rating: {rating}</li>"
	+ f"<li>Comments: {comments}</li>"
	+ "</ul>")

	sender_email = 'email@example.com'
	reciever_email = 'email2@example.com'

	msg = MIMEText(message, 'html')
	msg['Subject'] = 'Lexus Feedback'
	msg['From'] = sender_email
	msg['To'] = reciever_email

	with smtplib.SMTP(smtp_server, port) as server:
		server.login(login, password)
		server.sendmail(sender_email, reciever_email, msg.as_string())
	print('sent mail')