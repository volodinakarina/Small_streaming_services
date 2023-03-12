from project.models import User, Favorite, Movie
from sqlalchemy.orm import scoped_session


class UserDAO:

    def __init__(self, db_session: scoped_session) -> None:
        self._db_session = db_session

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()

    def create(self, new_user):
        entity = User(**new_user)
        self._db_session.add(entity)
        self._db_session.commit()
        return entity

    def update(self, user):
        self._db_session.add(user)
        self._db_session.commit()

    def get_favorites(self, uid):
        return self._db_session.query(Movie).join(Favorite).filter(Favorite.user_id == uid).all()

    def add_favorite(self, uid, mid):
        entity = Favorite(**{'user_id': uid, 'movie_id': mid})
        self._db_session.add(entity)
        self._db_session.commit()

    def delete_favorite(self, uid, mid):
        entity = self._db_session.query(Favorite).filter(Favorite.user_id == uid,
                                                         Favorite.movie_id == mid).first()
        self._db_session.delete(entity)
        self._db_session.commit()