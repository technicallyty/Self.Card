import logging
import re
import validators
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
import uuid
from .models import Domain, Components
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
  return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
  email = current_user.email
  testEndpoint = Domain.query.filter_by(owner=email).first()
  cards = None
  if testEndpoint:
    testEndpoint = testEndpoint.endpoint
    cards = Components.query.filter_by(endpoint=testEndpoint).all()
  return render_template('profile.html', name=current_user.name, endpoint=testEndpoint, cards=cards)




@main.route('/create-endpoint')
@login_required
def create_endpoint():
  return render_template('create-endpoint.html')


@main.route('/create-endpoint', methods=['POST'])
@login_required
def create_endpoint_post():
  endpoint = request.form.get('endpoint')
  if not re.match("^[A-Za-z0-9_-]*$", endpoint):
    flash("Your endpoint can only include letters, numbers, -, and _.")
    return redirect(url_for('main.create_endpoint'))
  else:
    email = current_user.email
    checkEndpoint = Domain.query.filter_by(owner=email).first()
    check2 = Domain.query.filter_by(endpoint=endpoint).first()
    if checkEndpoint:
      flash('You already have an endpoint.')
      return redirect(url_for('main.create_endpoint'))
  
    if check2:
      flash("Endpoint already exists.")
      return redirect(url_for('main.create_endpoint'))

    selfEndpoint = Domain(endpoint=endpoint, owner=email)
    db.session.add(selfEndpoint)
    db.session.commit()

    return redirect(url_for('main.profile'))


@main.route("/delete-card", methods=["DELETE"])
@login_required
def delete_card():
  card_id = request.form.get("card_id")
  card = Components.query.filter_by(id=card_id).first()

  domain = Domain.query.filter_by(endpoint=card.endpoint).first()

  print(domain.endpoint, flush=True)
  print(card.endpoint, flush=True)
  print(domain.owner, flush=True)
  if not domain.owner == current_user.email:
    return jsonify(status="error")

  if card:
    db.session.delete(card)
    db.session.commit()
    return jsonify(status="success")
  else:
    return jsonify(status="error")
  
@main.route('/create')
@login_required
def create():
  email = current_user.email
  hasDomain = Domain.query.filter_by(owner=email).first()
  if hasDomain:
    return render_template('create.html', hasDomain=True)
  else:
    return render_template('create.html', hasDomain=False)


@main.route('/create', methods=['POST'])
@login_required
def create_new_card():
  email = current_user.email
  userEndpoint = Domain.query.filter_by(owner=email).first()
  userEndpoint = userEndpoint.endpoint
  title = request.form.get('card-title')
  body = request.form.get('card-body')
  buttonTitle = request.form.get('card-button-title') or None
  buttonLink = request.form.get('card-button-link') or None
  if buttonLink and not buttonTitle:
    buttonLink = None
    flash("Please add a title to your button")
    return redirect(url_for('main.create'))
  if buttonTitle and not buttonLink:
    buttonTitle = None
    flash("Please add a link to your button.")
    return redirect(url_for('main.create'))

  if buttonLink and buttonTitle:
    validLink = validators.url(buttonLink)
    if not validLink:
      flash("Please input a valid link for your button")
      return redirect(url_for('main.create'))

  if(title and body):
    newComponent = Components(endpoint=userEndpoint,title=title, content=body, button=buttonTitle, buttonAction=buttonLink)
    db.session.add(newComponent)
    db.session.commit()
  return redirect(url_for('main.profile'))


@main.route('/<endpoint>', methods=['GET'])
def user_profile(endpoint):
  cards = Components.query.filter_by(endpoint=endpoint).all()

  if not cards:
    return render_template('404.html'),404
  else:
    return render_template('user-profile.html', cards=cards, name=endpoint)