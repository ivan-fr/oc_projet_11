from flask import render_template, request, flash, redirect, url_for

from grandpyapp.managers.parser import parse_sentence
from grandpyapp.managers.googlemaps import parse_geolocate_response
import grandpyapp.managers.wikipedia as wikipedia
from grandpyapp import app, db
from grandpyapp.forms import LoginForm, RegistrationForm, EditProfileForm, \
    AdressForm
from grandpyapp.models import User

from flask_login import current_user, login_user, logout_user, login_required

from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

import json
import logging
import os


@app.route('/', methods=['GET', 'POST'])
def index():
    """Render the index page."""
    form = AdressForm()

    if request.is_xhr:
        google_maps_parsed = None
        errors_form = None

        if form.validate_on_submit():
            adress = form.street.data + ", " + form.postal_code.data + ' ' \
                     + form.city.data + ", " + form.countries.data

            google_maps_parsed = parse_geolocate_response(
                adress, from_country=form.countries.data)

        if form.errors:
            errors_form = list(form.errors.items())

        return json.dumps({
            'google_maps_parsed': google_maps_parsed,
            'errors_form': errors_form
        })

    url = "https://maps.googleapis.com/" \
          "maps/api/js?key={}".format(app.config["GOOGLE_API_KEY"])

    return render_template('index.html', url_google_map_api=url,
                           form=form)


@app.route('/post_ask/', methods=['POST'])
def post_ask():
    """traitment of the ask request
    :return google_maps and wikipedia response"""
    if request.form.get('ask'):
        google_maps_parsed = {}
        wikipedia_parsed = {}
        _parse_sentence = parse_sentence(request.form['ask'])

        if _parse_sentence:
            try:
                google_maps_parsed = parse_geolocate_response(_parse_sentence)

                wiki_search_list = wikipedia.search(
                    google_maps_parsed['asked_address'], suggestion=False)

                if not wiki_search_list:
                    wiki_search_list = wikipedia.search(
                        google_maps_parsed['formatted_address'],
                        suggestion=False)

                if not wiki_search_list:
                    wiki_search_list = wikipedia.geosearch(
                        latitude=google_maps_parsed['location']['lat'],
                        longitude=google_maps_parsed['location']['lng'],
                    )

                if wiki_search_list:
                    wikipedia_page = wikipedia.page(wiki_search_list[0])
                    wikipedia_parsed['_summary'] = wikipedia_page.summary(
                        sentences=2)
                    wikipedia_parsed['url'] = wikipedia_page.url
            except Exception as e:
                logging.exception(e)

        return json.dumps({
            'google_maps_parsed': google_maps_parsed,
            'wikipedia_parsed': wikipedia_parsed
        })


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Déjà connecté')
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        flash('Requête pour se connecter avec l\'utilisateur {},'
              ' se souvenir de moi={}'.format(form.username.data,
                                              form.remember_me.data))

        _user = User.query.filter_by(username=form.username.data).first()

        if _user is None or not _user.check_password(form.password.data):
            flash('Prénom ou mot de passe invalide.')
            return redirect(url_for('login'))

        login_user(_user, remember=form.remember_me.data)
        flash('Connexion réussi.')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('Déconnexion réussi.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Déjà connecté')
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        adress = form.street.data + ", " + form.postal_code.data + ' ' \
                 + form.city.data + ", " + form.countries.data

        try:
            google_maps_parsed = parse_geolocate_response(
                adress, from_country=form.countries.data)

            file = form.photo.data
            filename = form.username.data + '_' + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            user = User(username=form.username.data,
                        photo=filename,
                        street=form.street.data,
                        postal_code=form.postal_code.data,
                        city=form.city.data,
                        countries=form.countries.data,
                        place_id=google_maps_parsed['place_id'])
            user.set_password(form.password.data)

            db.session.add(user)
            db.session.commit()
            flash('Félicitation, vous avez enregistrez un compte.')
            return redirect(url_for('login'))
        except Exception as e:
            logging.exception(e)
            flash('Une erreur est survenue, probablement que'
                  ' votre adresse est incorrect.')

    return render_template('register.html', form=form)


@app.route('/user/<username>', methods=['GET', 'POST'])
def user(username):
    _user = User.query.filter_by(username=username).first_or_404()
    context = {'show_form': False}

    if _user == current_user:
        form = EditProfileForm()
        adress_form = AdressForm()

        if form.validate_on_submit():
            file = form.photo.data
            filename = _user.username + '_' + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            try:
                os.remove(
                    os.path.join(app.config['UPLOAD_FOLDER'], _user.photo))
            except FileNotFoundError:
                pass

            _user.photo = filename
            db.session.commit()
            flash('Vos changements ont été sauvergardé.')

        elif adress_form.validate_on_submit():
            adress = adress_form.street.data + ", " \
                     + adress_form.postal_code.data + ' ' \
                     + adress_form.city.data + ", " \
                     + adress_form.countries.data

            try:
                google_maps_parsed = parse_geolocate_response(
                    adress, from_country=adress_form.countries.data)

                _user.street = adress_form.street.data
                _user.postal_code = adress_form.postal_code.data
                _user.city = adress_form.city.data
                _user.countries = adress_form.countries.data
                _user.place_id = str(google_maps_parsed['place_id'])

                db.session.commit()

                flash('Vos changements ont été sauvergardés.')

            except Exception as e:
                logging.exception(e)
                flash('Une erreur est survenue, probablement que'
                      ' votre adresse est incorrect.')

            form.errors = []

        context['show_form'] = True
        context['form'] = form
        context['adress_form'] = adress_form

    return render_template('user.html', user=_user, **context)
