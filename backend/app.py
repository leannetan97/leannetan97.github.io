from flask import Flask
from flask import Flask, render_template
from flask_mail import Mail, Message
from flask import request
from flask import jsonify
from flask import Response
from flask_cors import CORS
import requests

app = Flask(__name__)

CORS(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587 # For TLS
app.config['MAIL_USERNAME'] = '#####@gmail.com'
app.config['MAIL_PASSWORD'] = '******'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = '#####@gmail.com'
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

# @app.route('/')
# def root():
#     return render_template("index.html")


@app.route("/send", methods = ['POST'])
def index():
	try:	
		name = request.form['Name']
		email = request.form['Email']
		subject = request.form['Subject']
		message = request.form['Message']
		captcha_response = request.form['g-recaptcha-response']

		email_subject = '[leannetan97.github.io] You got a message from ' + name
	   
		verified = verify(captcha_response)
		print ("Details :\n", name, email, subject, message, captcha_response)
		verified = True
		if verified:
			own_message =  '<b>Subject:</b> ' + subject + '<br><b>Sender Name:</b> ' + name + '<br><b>Sender Email:</b> ' + email + '<br><br>' + message
			msg = Message(email_subject, recipients = ['leannetan97@hotmail.com'], html = own_message)
			mail.send(msg)
			
			print ("Details :\n", name, email, subject, own_message)
			
			return jsonify({
					'status': 'verified',
					})

		return jsonify({
					'status': 'unverified',
					})
	except Exception as e:
		raise e
		return str(e)

def verify(token):
	SECRET_KEY = '*****************************************'
	recaptcha_req = requests.post('https://www.google.com/recaptcha/api/siteverify',data={'secret': SECRET_KEY, 'response': token})
	status_code = recaptcha_req.status_code
	return jsonify({
		'status_code': status_code,
		'success': recaptcha_req.json()['success']
	})

if __name__ == '__main__':
   app.run(debug = True)
