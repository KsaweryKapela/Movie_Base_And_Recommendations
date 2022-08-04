import time
from sqlalchemy.orm import lazyload, subqueryload, joinedload, selectinload, noload
from main import MoviesDatabase, UsersFilms, db, UserSuggestion, Actors, Directors, Genres


class MovieRecommendations:

    def __init__(self):
        self.points = 0
        self.actors_dict = {}
        self.genres_dict = {}
        self.directors_dict = {}
        self.writers_dict = {}
        self.year_dict = {}
        self.PG_dict = {}
        self.users_id_list = []
        self.clear_old_recommendations()

    @staticmethod
    def clear_old_recommendations():
        UserSuggestion.query.delete()
        db.session.commit()

    def prepare_score(self, movie, points):
        if movie.tag == 'heart':
            score = points * 2
        elif movie.tag == 'dislike':
            score = -(points * 2)
        elif movie.tag == 'bookmark':
            score = points
        elif movie.tag == 'ignore':
            score = -points
        return score

    def populate_dictionary(self, movie, column_name, dictionary_name, points):
        for item in column_name:
            if item in dictionary_name:
                dictionary_name[item.id] += self.prepare_score(movie, points)
            else:
                dictionary_name[item.id] = self.prepare_score(movie, points)

    def get_simple_dict(self, movie, item_def, dictionary_name, points):
        if item_def != '':
            if item_def in dictionary_name:
                dictionary_name[item_def] += self.prepare_score(movie, points)
            else:
                dictionary_name[item_def] = self.prepare_score(movie, points)



    def populate_all_dictionaries(self, user_id):
        for movie in UsersFilms.query.filter(UsersFilms.user_id == user_id).all():
            self.users_id_list.append(movie.movie_id)

            self.populate_dictionary(movie, movie.movies_database.actors, self.actors_dict, 25)
            self.populate_dictionary(movie, movie.movies_database.genres, self.genres_dict, 25)
            self.populate_dictionary(movie, movie.movies_database.director_of, self.directors_dict, 25)
            self.populate_dictionary(movie, movie.movies_database.writer_of, self.writers_dict, 12.5)
            self.get_simple_dict(movie, movie.movies_database.release_date[:4], self.year_dict, 12.5)
            self.get_simple_dict(movie, movie.movies_database.PG, self.PG_dict, 25)

    def clean_up_dictionaries(self):
        self.actors_dict = {}
        self.genres_dict = {}
        self.directors_dict = {}
        self.writers_dict = {}
        self.year_dict = {}
        self.PG_dict = {}
        self.users_id_list = []

    def add_points(self, table_name, dict_name):
        for item in table_name:
            if item.id in dict_name.keys():
                self.points += dict_name[item.id]

    def get_liked_items(self, dictionary):
        liked_items = []
        for key in dictionary:
            if dictionary[key] > 25:
                liked_items.append(key)
        return liked_items

    def give_points_for_score(self, movie):
        if movie.computed_critic_score:
            self.points += movie.computed_critic_score * 2

        if movie.computed_audience_score:
            self.points += movie.computed_audience_score * 2

    def split_the_points(self, movie):
        self.points = 0

        self.add_points(movie.actors, self.actors_dict)
        self.add_points(movie.genres, self.genres_dict)
        self.add_points(movie.director_of, self.directors_dict)
        self.add_points(movie.writer_of, self.writers_dict)

        if int(movie.release_date[:4]) - 1 in self.year_dict.keys():
            self.points += self.year_dict[movie.release_date[:4]]
        elif int(movie.release_date[:4]) in self.year_dict.keys():
            self.points += self.year_dict[movie.release_date[:4]]
        elif int(movie.release_date[:4]) + 1 in self.year_dict.keys():
            self.points += self.year_dict[movie.release_date[:4]]

        if movie.PG in self.PG_dict.keys():
            self.points += self.PG_dict[movie.PG]

        self.give_points_for_score(movie)

    def update_recommendations(self, user_id):
        self.clean_up_dictionaries()

        self.populate_all_dictionaries(user_id)

        for movie in MoviesDatabase.query. \
                filter(Actors.id.in_(self.get_liked_items(self.actors_dict))). \
                filter(MoviesDatabase.PG.in_(self.get_liked_items(self.PG_dict))). \
                filter(MoviesDatabase.id.notin_(self.users_id_list)). \
                join(MoviesDatabase.actors). \
                options(joinedload(MoviesDatabase.actors)). \
                join(MoviesDatabase.genres). \
                options(joinedload(MoviesDatabase.genres)). \
                join(MoviesDatabase.director_of). \
                options(joinedload(MoviesDatabase.director_of)). \
                all():

            self.split_the_points(movie)
            new_movie = UserSuggestion(title=movie.title, points=self.points)
            db.session.add(new_movie)
        db.session.commit()


recommend = MovieRecommendations()

start = time.perf_counter()

recommend.update_recommendations(2)

end = time.perf_counter()
print(end - start)
