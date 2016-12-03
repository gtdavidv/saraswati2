from flask import Flask, Blueprint, render_template, session
from random import randint
from db import *

basic = Blueprint('basic', __name__)

@basic.route('/about')
def about():
	return render_template("about.html")

@basic.route('/faq')
def faq():
	return render_template("faq.html")

@basic.route('/contact')
def contact():
	return render_template("contact.html")
