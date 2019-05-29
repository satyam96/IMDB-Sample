from flask import Flask, jsonify, Blueprint
from flask import render_template, request, url_for, flash, abort, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost:3306/deltaX'
# user : pwd @ host:portNumber / db_name
app.config['SQLALCHEMY_TRACE_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'random_value_string'

db = SQLAlchemy(app)       #connection to the database
db.init_app(app)

# association table between Actors and Movies

association = db.Table('actors_identifier',
		db.Column('actors_id', db.Integer, db.ForeignKey('actors.aid')),
		db.Column('movies_id', db.Integer, db.ForeignKey('movies.mid'))
	)

class Actors(db.Model):
	__tablename__ = 'actors'
	aid = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable = False)
	sex = db.Column(db.String(50), nullable = False)
	dob = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	bio = db.Column(db.String(200), nullable = False)
	actors_in_movies = db.relationship("Movies", secondary = association)

	def __init__(self, name, sex, dob, bio):
		self.name = name
		self.sex = sex
		self.dob = dob
		self.bio = bio


class Movies(db.Model):
	__tablename__ = 'movies'
	mid = db.Column(db.Integer, primary_key = True, auto_increment = True)
	name = db.Column(db.String(100), nullable = False)
	year_of_release = db.Column(db.Integer, nullable = False)
	plot = db.Column(db.String(200), nullable = False)
	poster = db.Column(db.String(100), nullable = False)
	actors = db.Column(db.String(100), nullable = False)
	producer = db.Column(db.String(100), nullable = False)
	# movies_actors = db.relationship("Actors", secondary = association)
	# movie_producers = db.relationship("Producers", ForeignKey('producers.pid'))
	def __init__(self,name,year_of_release,plot,poster,actors,producer):
		self.name = name
		self.year_of_release = year_of_release
		self.plot = plot
		self.poster = poster
		self.actors = actors
		self.producer = producer
		

class Producers(db.Model):
	__tablename__ = 'producers'
	pid = db.Column(db.Integer, primary_key = True, auto_increment = True)
	name = db.Column(db.String(100), nullable = False)
	sex = db.Column(db.String(50), nullable = False)
	dob = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
	bio = db.Column(db.String(200), nullable = False)

	def __init__(self, name, sex, dob, bio):
		self.name = name
		self.sex = sex
		self.dob = dob
		self.bio = bio

@app.route("/", methods=['GET','POST'])
def movies():
	return render_template('movie.html', movies = Movies.query.all())

@app.route("/new_movie", methods=['GET', 'POST'])
def add_new_movie():
	if request.method == 'GET':
		return render_template('add_new_movie.html', act = Actors.query.all(), prod = Producers.query.all())
	elif request.method == 'POST':
		add_new = Movies(request.form['movie_name'],
						 request.form['year_of_release'],
						 request.form['plot'],
						 request.form['poster'],
						 request.form['actors[]'],
						 request.form['prod'])
		db.session.add(add_new)
		db.session.commit()
		return redirect("/")

@app.route("/new_actors", methods=['GET','POST']) 
def actors():
	if request.method == 'GET':
		return render_template('add_actor.html')
	elif request.method == 'POST':
		add_new_actor = Actors(request.form['actor_name'],
							   request.form['sex'],
							   request.form['dob'],
							   request.form['bio'])
		db.session.add(add_new_actor)
		db.session.commit()
		return redirect('/new_movie')

@app.route("/new_producers", methods=['GET','POST'])
def producers():
	if request.method == 'GET':
		return render_template('add_producer.html')
	elif request.method == 'POST':
		add_new_producer = Producers(request.form['producer_name'],
							   	  	 request.form['sex'],
							   	  	 request.form['dob'],
							      	 request.form['bio'])
		db.session.add(add_new_producer)
		db.session.commit()
		return redirect('/new_movie')

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)