import json

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    validators, SelectField

from config import COUNTRIES_FILE
from grandpyapp.models import User


class LoginForm(FlaskForm):
    username = StringField('Prénom', validators=[validators.DataRequired(),
                                                 validators.Length(min=4,
                                                                   max=25)])
    password = PasswordField('Mot de passe',
                             validators=[validators.DataRequired(),
                                         validators.Length(min=4, max=35)])
    remember_me = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class RegistrationForm(FlaskForm):
    username = StringField('Prénom', validators=[validators.DataRequired()])

    password = PasswordField('Mot de passe',
                             validators=[validators.DataRequired()])
    password2 = PasswordField(
        'Confirmez', validators=[validators.DataRequired(),
                                 validators.EqualTo('password')])

    photo = FileField(validators=[FileRequired(),
                                  FileAllowed(['jpg', 'png', 'jpeg'],
                                              'Images only!')])

    street = StringField('Rue', validators=[validators.DataRequired(),
                                            validators.Length(max=150)])
    city = StringField('Ville', validators=[validators.DataRequired(),
                                            validators.Length(max=50)])
    postal_code = StringField('Code postal',
                              validators=[validators.DataRequired(),
                                          validators.Length(max=20)])

    with open(COUNTRIES_FILE, "r", encoding="utf-8") as file:
        countries = SelectField('Pays', choices=list((json.load(file)).items()),
                                validators=[validators.DataRequired()])

    submit = SubmitField('Créer un compte')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise validators.ValidationError('Utilisez un autre prénom.')


class EditProfileForm(FlaskForm):
    photo = FileField(validators=[FileRequired(),
                                  FileAllowed(['jpg', 'png', 'jpeg'],
                                              'Images only!')])

    submit = SubmitField('Éditer mon profile')


class AdressForm(FlaskForm):
    street = StringField('Rue', validators=[validators.DataRequired(),
                                            validators.Length(max=150)])
    city = StringField('Ville', validators=[validators.DataRequired(),
                                            validators.Length(max=50)])
    postal_code = StringField('Code postal',
                              validators=[validators.DataRequired(),
                                          validators.Length(max=20)])

    with open(COUNTRIES_FILE, "r", encoding="utf-8") as file:
        countries = SelectField('Pays', choices=list((json.load(file)).items()),
                                validators=[validators.DataRequired()])

    submit = SubmitField('Envoyer')


class AskForm(FlaskForm):
    ask = StringField('ask', validators=[validators.DataRequired(),
                                         validators.Length(max=200)],
                      render_kw={"placeholder": "Salut GrandPy ! "
                                                "Est-ce que tu connais "
                                                "l'adresse d'OpenClassrooms ?",
                                 "autocomplete": "off"})

    with open(COUNTRIES_FILE, "r", encoding="utf-8") as file:
        _list = [('', '')] + list((json.load(file)).items())
        countries = SelectField('Pays', choices=_list)

    submit = SubmitField('Envoyer')
