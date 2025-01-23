from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///top10-movies.db'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False) 
    description: Mapped[str] = mapped_column(String(250), nullable=False) 
    rating: Mapped[float] = mapped_column(Float, nullable=False) 
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()

class EditForm(FlaskForm):
    rating = FloatField(label="Your Rating out of 10 e.g. 7.3", validators=[DataRequired()])
    review = StringField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")

class AddForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add Movie")


@app.route("/")
def home():
    with app.app_context():
        all_movies = db.session.execute(db.select(Movie)).scalars().all()
    return render_template("index.html", movies=all_movies)

@app.route('/edit/<movie_title>', methods=['GET','POST'])
def edit(movie_title):
    edit_form = EditForm()
    with app.app_context():
        movie = db.session.execute(db.select(Movie).where(Movie.title == movie_title)).scalar()
        if request.method == 'POST':
            movie.rating = request.form['rating']
            movie.review = request.form['review']
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('edit.html', form=edit_form)

@app.route('/delete/<movie_title>', methods=['GET','POST'])
def delete(movie_title):
    with app.app_context():
        movie_to_delete = db.session.execute(db.select(Movie).where(Movie.title == movie_title)).scalar()
        db.session.delete(movie_to_delete)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=['GET','POST'])
def add():
    add_form = AddForm()
    if request.method == 'POST' and add_form.validate_on_submit():
        return redirect('home')
    return render_template('add.html', form=add_form)

if __name__ == '__main__':
    app.run(debug=True)


# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
#     )

# second_movie = Movie(
#     title="Avatar The Way of Water",
#     year=2022,
#     description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#     rating=7.3,
#     ranking=9,
#     review="I liked the water.",
#     img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
# )


# with app.app_context():
#     db.session.add(new_movie)
#     db.session.commit()