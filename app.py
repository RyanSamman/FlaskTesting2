import os
from send_mail import send_mail
from werkzeug import datastructures
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# https://gist.github.com/bradtraversy/0029d655269c8a972df726ed0ac56b88

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None: raise Exception("Database URL was not defined")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
	__tablename__ = 'feedback'
	id = db.Column(db.Integer, primary_key=True)
	customer = db.Column(db.String(200), unique=True)
	dealer = db.Column(db.String(200))
	rating = db.Column(db.Integer)
	comments = db.Column(db.Text())

	def __init__(self, customer, dealer, rating, comments):
		self.customer = customer
		self.dealer = dealer
		self.rating = rating
		self.comments = comments


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')
	

if __name__ == "__main__":
	if os.getenv("FLASK_ENV") == 'dev':
		print('Debugging time')
		app.debug = True

	app.run()
