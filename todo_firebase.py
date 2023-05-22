import pyrebase
import pickle
import os

import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccount.json")

firebase_admin.initialize_app(
    cred,
    {'datebaseURL': "https://app-todo-80542-default-rtdb.firebaseio.com/"}
)

firebaseConfig = {
    'apiKey': "AIzaSyB3lJZAEJErkD08VEoKFjDdVe7lNjuau2U",
    'authDomain': "app-todo-80542.firebaseapp.com",
    'databaseURL': "https://app-todo-80542-default-rtdb.firebaseio.com",
    'projectId': "app-todo-80542",
    'storageBucket': "app-todo-80542.appspot.com",
    'messagingSenderId': "138718095242",
    'appId': "1:138718095242:web:da44f2d2f0fe0348948a73"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

class DB:

    users = None
    todos = None

    @staticmethod
    def connect_db():

        try:
            DB.todos = db.reference('/todos')
        except Exception as e:
            print(e)

    def read_todos(self):
        return DB.todos.get() if DB.todos else {}

    def search_todos(self, key, search):
        res = {}
        for k, v in DB.todos.get().items():
            if search in v[key]:
                res[k] = v
        return res

    def get_todos_statistics(self):
        for item in DB.todos.get().items():
            pass

    def insert_todo(self, values):
        new_ref = DB.todos.push()
        new_key = not new_ref.key
        new_ref.set(values)
        return new_key

    def delete_todo(self, key):
        DB.todos.child(key).set({})

    def update_todos(self, key, value):
        DB.todos.child(key).update(value)

    def update_task_state(self, key, value):
        DB.todos.child(key).update(value)

class Auth:

    @staticmethod
    def create_user(name, email, password):
        try:
            firebase_auth.create_user(
                email = email,
                password = password,
                display_name = name)
            return None
        except Exception as e:
            return e
    @staticmethod
    def reset_password(email):
        try:
            auth.send_password_reset_email(email)
            return not None
        except:
            return None
    @staticmethod
    def login_user(email, password):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            return user['idToken']
        except:
            return None
    @staticmethod
    def store_session(token):
        if os.path.exists('token.pickle'):
            os.remove('token.pickle')
        with open('token.pickle', 'wb') as f:
            pickle.dump(token, f)
    @staticmethod
    def load_token():
        try:
            with open('token.pickle', 'rb') as f:
                token = pickle.load(f)
            return token
        except:
            return None
    @staticmethod
    def authenticated_token(token):
        try:
            result = firebase_auth.verify_id_token(token)
            return result['user_id']
        except:
            return None
    @staticmethod
    def get_name(token):
        try:
            result = firebase_auth.verify_id_token(token)
            return result['name']
        except:
            return None
    @staticmethod
    def revoke_token(token):
        firebase_auth.revoke_refresh_tokens(Auth.authenticated_token(token))
        if os.path.exists('token.pickle'):
            os.remove('token.pickle')