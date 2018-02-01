#!/usr/bin/env python

import os
from flask import Flask, url_for, request, redirect, flash, render_template, g, send_from_directory
import flask_login
from tools import allowed_file
from werkzeug.utils import secure_filename
from epubzilla.epubzilla import Epub
from epub_thumbnailer import find_cover
from settings import app, db, login_manager
from models import User, Book
import zipfile

@app.route('/register' , methods=['POST'])
def register():
    if request.method == 'POST':
        user = User(request.form['username'] , request.form['password'], request.form['email'], False)
        try:
            db.session.add(user)
            db.session.commit()
            flash('User successfully registered')
        except:
            flash('Error')
        return redirect(url_for('users'))

@app.route('/')
@flask_login.login_required
def list():
    g.books = Book.query.order_by(Book.registered_on).all()
    return render_template('index.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash("You have to be logged in to access this page.")
    return redirect(url_for('login', next=request.path))

@app.route('/users')
@flask_login.login_required
def users():
    if g.user.admin:
        g.users = User.query.order_by(User.username).all()
        return render_template('users.html')
    else:
        flash('Access Unauthorized')
        return redirect('/')

@app.route('/users/<id>/delete')
@flask_login.login_required
def delete_user(id):
    obj = User.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<id>/edit')
@flask_login.login_required
def edit_user(id):
    g.obj = User.query.get(id)
    db.session.commit()
    return redirect('/users')

@app.route('/upload', methods=['POST'])
@flask_login.login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect('/')
    file = request.files['file']
    if file and allowed_file(file.filename):
        epub = Epub.from_file(file)
        epub_file_ext = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(epub_file_ext)
        find_cover(epub_file_ext)
        epub_file = os.path.splitext(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))[0]
        book = Book(secure_filename(file.filename.split('.')[0]), epub.title, epub.author)
        with zipfile.ZipFile(file,"r") as zip_ref:
            zip_ref.extractall(epub_file)
        db.session.add(book)
        db.session.commit()
        flash('Upload sucessful')
    else:
        flash('Epub only is allowed')
    return redirect('/')

@app.route('/books/media/<path:path>')
@flask_login.login_required
def show(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)

@app.route('/books/<id>/delete')
@flask_login.login_required
def delete(id):
    obj = Book.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    return redirect('/')

@app.route('/books/<id>/read')
@flask_login.login_required
def read(id):
    g.read_book = Book.query.get(id)
    return render_template('read.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    nb_user = User.query.order_by(User.username).count()
    if nb_user == 0:
        admin = User('admin', 'admin', 'admin@localhost', True)
        db.session.add(admin)
        db.session.commit()
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(username=username).first()
    if registered_user is None:
        flash('Username is invalid', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Password is invalid', 'error')
        return redirect(url_for('login'))
    flask_login.login_user(registered_user, remember=remember_me)
    flash('Welcome to Bookstore')
    return redirect(request.args.get('next') or '/')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/')

@app.route('/settings')
@flask_login.login_required
def settings():
    return 'Settings'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = flask_login.current_user

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
