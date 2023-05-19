from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-films-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# THIS CLASS CREATES QUERIES AND UPDATES RECORDS IN DATABASE
class DatabaseManager:
    def create_entry_and_return_id(self, title, year, description, img_url, rating=0.0, ranking=0, review=""):
        with app.app_context():
            new_film = Film(
                title=title,
                year=year,
                description=description,
                rating=rating,
                ranking=ranking,
                review=review,
                img_url=img_url
            )
            db.session.add(new_film)
            db.session.commit()
            self.refresh_all_rankings()
            return self.select_film(new_film.id)

    def get_all_films(self):
        with app.app_context():
            films = db.session.query(Film).order_by(Film.ranking).all()
            return films

    def select_film(self, film_id):
        with app.app_context():
            film = db.session.get(Film, film_id)
            return film

    def delete_film(self, film_id):
        with app.app_context():
            film_selected = self.select_film(film_id)
            db.session.delete(film_selected)
            db.session.commit()

    def update_film(self, film_id, new_rating, new_review):
        with app.app_context():
            film_selected = db.session.get(Film, film_id)
            film_selected.rating = new_rating
            film_selected.review = new_review
            db.session.commit()
        self.refresh_all_rankings()

    def refresh_all_rankings(self):
        with app.app_context():
            all_sorted_films = db.session.query(Film).order_by(Film.rating).all()
            for i in range(len(all_sorted_films)):
                all_sorted_films[i].ranking = len(all_sorted_films) - i
            db.session.commit()


# CREATE TABLE
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float(), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    # This will allow each object to be identified by its title when printed.
    def __repr__(self):
        return f'<Film {self.title}>'


db.create_all()
