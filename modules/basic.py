from flask import Flask, Blueprint, render_template, session
from random import randint
from db import *

basic = Blueprint('basic', __name__)

@basic.route('/')
def index():
	if session.get('session_id') is None:
		session['session_id'] = str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))
		
	return render_template("index.html", messages = message.query.filter_by(session_id=session['session_id']))

@basic.route('/about')
def about():
	return render_template("about.html")

@basic.route('/faq')
def faq():
	return render_template("faq.html")

@basic.route('/contact')
def contact():
	return render_template("contact.html")
