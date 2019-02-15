from grandpyapp import app, db
from flask import url_for
import urllib.request
from io import BytesIO
from .mock_data_views import mock_data_view
from grandpyapp.models import User
import json


def mockreturn(request):
    return BytesIO(mock_data_view['requests'][request].encode())


class TestViews:
    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config[
            'SQLALCHEMY_DATABASE_URI_TEST']
        app_context = app.test_request_context()
        app_context.push()
        cls.client = app.test_client()
        db.create_all()
        cls.app = app

        cls.user = User(username='ivan',
                        photo='1.jpeg',
                        street='tour eiffel',
                        postal_code='75019',
                        city='paris',
                        countries='france',
                        place_id="sdfjpdsojsdo")
        cls.user.set_password('password')

        db.session.add(cls.user)
        db.session.commit()

    def test_get_index_view(self):
        rv = self.client.get(url_for('index'))
        assert rv.status_code == 200

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_post_index_view(self, monkeypatch):
        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        response = self.client.post(url_for('index'),
                                    data=dict(
                                        street='tour eiffel',
                                        city='paris',
                                        postal_code='75',
                                        countries='FR',
                                    ),
                                    headers=[
                                        ('X-Requested-With', 'XMLHttpRequest')])

        _dict = json.loads(response.data)
        assert list(_dict.keys()) == ["google_maps_parsed", "errors_form"]
        assert _dict["errors_form"] is None
        assert _dict["google_maps_parsed"] is not None

    def test_invalide_post__index_view(self, monkeypatch):
        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        response = self.client.post(url_for('index'),
                                    data=dict(
                                        street='tour eiffel',
                                        postal_code='75',
                                    ),
                                    headers=[
                                        ('X-Requested-With', 'XMLHttpRequest')])

        _dict = json.loads(response.data)
        assert list(_dict.keys()) == ["google_maps_parsed", "errors_form"]
        assert _dict["google_maps_parsed"] is None
        assert _dict["errors_form"] is not None

    def test_login_logout(self):
        """Make sure login and logout works."""

        rv = self.login('ivan', 'password')
        assert 'Connexion réussi.' in rv.data.decode('utf-8')

        rv = self.login('ivan', 'password')
        assert 'Déjà connecté' in rv.data.decode('utf-8')

        rv = self.logout()
        assert 'Déconnexion réussi.' in rv.data.decode('utf-8')

        rv = self.login('ivano', 'fakepassword')
        assert 'Prénom ou mot de passe invalide.' in rv.data.decode('utf-8')

    def test_get_alrealy_connected_register_view(self):
        self.login('ivan', 'password')
        response = self.client.get(url_for('register'), follow_redirects=True)
        assert 'Déjà connecté' in response.data.decode('utf-8')
        self.logout()

    def test_register_view(self, monkeypatch):
        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        rv = self.client.get(url_for('register'))
        assert rv.status_code == 200

        rv = self.client.post(url_for('register'))
        assert rv.status_code == 200

    def test_user_views(self, monkeypatch):
        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        rv = self.client.get(url_for('user', username=self.user.username))
        assert rv.status_code == 200

        rv = self.client.post(url_for('user', username=self.user.username))
        assert rv.status_code == 200

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """
        db.session.remove()
        db.drop_all()
