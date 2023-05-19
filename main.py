import os

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap

from api_manager import ApiManager
from database_manager import DatabaseManager
from flask_forms import EditFilmForm, AddFilmForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

Bootstrap(app)

database_manager = DatabaseManager()
api_manager = ApiManager()


@app.route("/")
def home():
    # SHOW ALL FILMS FROM DB ON MAIN PAGE
    all_films = database_manager.get_all_films()
    return render_template("index.html", films=all_films)


@app.route("/edit", methods=['GET', 'POST'])
def edit_film():
    film_id = request.args.get('id')
    film_selected = database_manager.select_film(film_id)
    form = EditFilmForm()
    if form.validate_on_submit():
        # UPDATE RECORD IN DB AND REDIRECT TO HOME PAGE
        database_manager.update_film(
            film_id,
            new_rating=float(form.new_film_rating.data),
            new_review=str(form.new_film_review.data)
        )
        return redirect(url_for('home'))
    return render_template('edit.html', film=film_selected, form=form)


@app.route("/delete", methods=['GET', 'POST'])
def delete_film():
    # DELETE RECORD IN DB BY FILM ID AND REDIRECT TO HOME PAGE
    film_id = request.args.get('id')
    database_manager.delete_film(film_id)
    return redirect(url_for('home'))


@app.route("/add", methods=['GET', 'POST'])
def add_film():
    form = AddFilmForm()
    if form.validate_on_submit():
        # GET ALL AVAILABLE MOVIES BY TITLE FROM THE API AND ONCE ONE IS SELECTED REDIRECT TO SELECT PAGE
        all_movies = []
        title = form.title.data
        results = api_manager.get_films_by_title(title)
        for movie in results:
            original_title = movie['original_title']
            original_year = movie['release_date']
            id = movie['id']
            movie_dict = {'title': original_title, 'date': original_year, 'id': id}
            all_movies.append(movie_dict)
        return render_template('select.html', movies=all_movies)
    return render_template('add.html', form=form)


@app.route('/find_movie', methods=['GET', 'POST'])
def find_movie():
    movie_id = request.args.get('id')
    if movie_id:
        # THIS PAGE IS VISIBLE ONLY AFTER SELECTING THE FILM
        #  GETS ALL DATA ABOUT MOVIE FROM THE API BY ID AND ADDS IT TO DB
        movie_data = api_manager.get_film_details(movie_id)
        new_movie = database_manager.create_entry_and_return_id(
            title=movie_data['original_title'],
            year=movie_data['release_date'][:4],
            description=movie_data['overview'],
            img_url=movie_data['poster_url']
        )
        return redirect(url_for('edit_film', id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
