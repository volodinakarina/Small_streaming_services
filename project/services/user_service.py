from project.exceptions import ItemNotFound
from project.tools.security import generate_password_hash, compose_passwords
from project.dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO) -> None:
        self.dao = dao

    def get_by_email(self, email):
        if user := self.dao.get_by_email(email):
            return user
        raise ItemNotFound(f'User with email "{email}" not exists.')

    def create(self, user_data):
        if self.dao.get_by_email(user_data['email']):
            return None
        user_data['password'] = self.generate_hash(user_data['password'])
        return self.dao.create(user_data)

    def patch(self, user_data):
        email = user_data.get("email")
        user = self.get_by_email(email)

        if 'name' in user_data:
            user.name = user_data.get('name')
        if 'surname' in user_data:
            user.surname = user_data.get('surname')
        if 'favourite_genre' in user_data:
            user.favourite_genre = int(user_data.get('favourite_genre'))

        self.dao.update(user)

    def update(self, user_data):
        email = user_data.get("email")
        user = self.get_by_email(email)
        if self.compare_passwords(user.password, user_data['old_password']):
            user.password = self.generate_hash(user_data['new_password'])
            self.dao.update(user)

    def get_favorites(self, email):
        if user := self.dao.get_by_email(email):
            uid = user.id
            return self.dao.get_favorites(uid)
        return ''

    def add_favorire(self, email, mid):
        if user := self.dao.get_by_email(email):
            uid = user.id
            self.dao.add_favorite(uid, mid)

    def delete_favorite(self, email, mid):
        if user := self.dao.get_by_email(email):
            uid = user.id
            self.dao.delete_favorite(uid, mid)

    def generate_hash(self, password):
        return generate_password_hash(password)

    def compare_passwords(self, password_hash, password):
        return compose_passwords(password_hash, password)