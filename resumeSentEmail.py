from flask import Flask
from flask_mail import Mail, Message
from flask import request
from flask import jsonify
from flask import Response
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lemonice0206@gmail.com'
app.config['MAIL_PASSWORD'] = 'icegmail0628'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

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
		print ("Details :\n", name, email, subject, own_message, captcha_response)
		if verified:
			own_message =  'Subject: ' + subject + '\n' + 'Sender： ' + name + '\n' + 'Sender email: ' + email + '\n\n' + message
			msg = Message(subject = email_subject, body = own_message, sender = email, recipients = ['leannetan97@hotmail.com'])
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
	SECRET_KEY = '6LfPc7YUAAAAAPwqZfLlqZ0fzqe_707IHCMeCQGE'
	recaptcha_req = requests.post('https://www.google.com/recaptcha/api/siteverify',data={'secret': SECRET_KEY, 'response': token})
	status_code = recaptcha_req.status_code
	return jsonify({
		'status_code': status_code,
		'success': recaptcha_req.json()['success']
	})

if __name__ == '__main__':
   app.run(debug = True)