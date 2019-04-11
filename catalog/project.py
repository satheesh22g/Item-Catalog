from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, State, TouristPlace, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "tourist place"


# Connect to Database
engine = create_engine(
    'sqlite:///tourism.db',
    connect_args={
        'check_same_thread': False},
    echo=True)
Base.metadata.bind = engine


# create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validating state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    # check if a user exists, if it doesn't make a new one

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width:250px; height:250px;border-radius:150px;"> '
    flash("you are Successfully logged in.")
    flash("%s" % login_session['username'])
    print ("done!")
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except BaseException:
        return None


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
        # disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("you are logged out ")
        return redirect(url_for('showState'))

    else:
        # If the token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Only Information about states and Tourist places
@app.route('/state/<int:state_id>/menu/JSON')
def stateJSON(state_id):
    state = session.query(State).filter_by(id=state_id).one()
    items = session.query(TouristPlace).filter_by(
        state_id=state_id).all()
    return jsonify(TouristPlaces=[i.serialize for i in items])


@app.route('/state/<int:state_id>/menu/<int:menu_id>/JSON')
def tourustplaceJSON(state_id, menu_id):
    TouristPlace = session.query(TouristPlace).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=TouristPlace.serialize)


@app.route('/state/JSON')
def statesJSON():
    states = session.query(State).all()
    return jsonify(states=[r.serialize for r in states])


# Show all states
@app.route('/')
@app.route('/state/')
def showState():
    states = session.query(State)
    return render_template('states.html', states=states)
# Create a new state


@app.route('/state/new/', methods=['GET', 'POST'])
def newState():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            newState = State(
                name=request.form['name'],
                user_id=login_session['user_id'])
        session.add(newState)
        flash('New State %s Successfully Created' % newState.name)
        session.commit()
        return redirect(url_for('showState'))
    else:
        return render_template('newState.html')


# Edit a state
@app.route('/state/<int:state_id>/edit/', methods=['GET', 'POST'])
def editState(state_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedState = session.query(State).filter_by(id=state_id).one()
    creator = getUserInfo(editedState.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("only creator can edit this place-" + creator.name)
        return redirect(url_for('showState'))
    if request.method == 'POST':
        if request.form['name']:
            editedState.name = request.form['name']
            flash('State Successfully Edited %s' % editedState.name)
            return redirect(url_for('showState'))
    else:
        return render_template('editState.html', state=editedState)


# Delete a state
@app.route('/state/<int:state_id>/delete/', methods=['GET', 'POST'])
def deleteState(state_id):
    if 'username' not in login_session:
        return redirect('/login')
    stateToDelete = session.query(State).filter_by(id=state_id).one()
    creator = getUserInfo(stateToDelete.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("only creator can delete this state- " + creator.name)
        return redirect(url_for('showState'))
    if request.method == 'POST':
        session.delete(stateToDelete)
        flash('%s Successfully Deleted' % stateToDelete.name)
        session.commit()
        return redirect(url_for('showState', state_id=state_id))
    else:
        return render_template('deleteState.html', state=stateToDelete)


# Show Toursit plces in a State
@app.route('/state/<int:state_id>/')
@app.route('/state/<int:state_id>/menu/')
def showPlace(state_id):
    state = session.query(State).filter_by(id=state_id).one()
    items = session.query(TouristPlace).filter_by(state_id=state_id).all()
    creator = getUserInfo(state.user_id)
    return render_template(
        'TouristPlaces.html',
        items=items,
        state=state,
        creator=creator,
        state_id=state_id)


# Create a new Tourist Place
@app.route('/state/<int:state_id>/menu/new/', methods=['GET', 'POST'])
def newTouristPlace(state_id):
    if 'username' not in login_session:
        return redirect('/login')
    state = session.query(State).filter_by(id=state_id).one()
    creator = getUserInfo(state.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("only creator can make changes- " + creator.name)
        return redirect(url_for('showState'))
    if request.method == 'POST':
        newItem = TouristPlace(
            user_id=state.user_id,
            name=request.form['name'],
            description=request.form['description'],
            distance=request.form['distance'],
            language=request.form['language'],
            state_id=state_id)
        session.add(newItem)
        session.commit()
        flash(
            'New Tourist place %s Item Successfully Created' %
            (newItem.name))
        return redirect(url_for('showPlace', state_id=state_id))
    else:
        return render_template('addTouristPlace.html', state_id=state_id)


# Edit a Tourist Place
@app.route(
    '/state/<int:state_id>/TouristPlace/<int:menu_id>/edit',
    methods=[
        'GET',
        'POST'])
def editTouristPlace(state_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(TouristPlace).filter_by(id=menu_id).one()
    state = session.query(State).filter_by(id=state_id).one()
    creator = getUserInfo(editedItem.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("only creator can edit this place-" + creator.name)
        return redirect(url_for('showState'))
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['distance']:
            editedItem.distance = request.form['distance']
        if request.form['language']:
            editedItem.language = request.form['language']
        session.add(editedItem)
        session.commit()
        flash('TouristPlace Successfully Edited')
        return redirect(url_for('showPlace', state_id=state_id))
    else:
        return render_template(
            'editTouristPlace.html',
            state_id=state_id,
            menu_id=menu_id,
            item=editedItem)


# Delete a Tourist Place
@app.route(
    '/state/<int:state_id>/menu/<int:menu_id>/delete',
    methods=[
        'GET',
        'POST'])
def deleteTouristPlace(state_id, menu_id):
    if 'username' not in login_session:
        return redirect('/login')
    stateToDelete = session.query(State).filter_by(id=state_id).one()
    placeToDelete = session.query(TouristPlace).filter_by(id=menu_id).one()
    creator = getUserInfo(stateToDelete.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("only creator can delete-" + creator.name)
        return redirect(url_for('showState'))
    if request.method == 'POST':
        session.delete(placeToDelete)
        session.commit()
        flash('TouristPlace is Successfully Deleted')
        return redirect(url_for('showPlace', state_id=state_id))
    else:
        return render_template(
            'deleteTouristPlace.html',
            item=placeToDelete,
            state_id=state_id)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    
