from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from wch_Sp import Base, Watchname, Watchlist, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///Watches.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Watches Store"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
w1x_c12= session.query(Watchname).all()


# login
@app.route('/login')
def showLogin():
    
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    w1x_c12 = session.query(Watchname).all()
    w1xes = session.query(Watchlist).all()
    return render_template('login.html',
                           STATE=state, w1x_c12=w1x_c12, w1xes=w1xes)
    # return render_template('myhome.html', STATE=state
    # w1x_c12=w1x_c12,w1xes=w1xes)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
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
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
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

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    U134 = User(name=login_session['username'], email=login_session[
                   'email'])
    session.add(U134)
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
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session
# Home


@app.route('/')
@app.route('/home')
def home():
    w1x_c12 = session.query(Watchname).all()
    return render_template('myhome.html',w1x_c12=w1x_c12)
# Watch Category for admins


@app.route('/watchStore')
def Watchstore():
    try:
        if login_session['username']:
            name = login_session['username']
            w1x_c12 = session.query(Watchname).all()
            w1xs = session.query(Watchname).all()
            w1xes = session.query(Watchlist).all()
            return render_template('myhome.html', w1x_c12=w1x_c12,
                                   w1xs=w1xs, w1xes=w1xes, uname=name)
    except:
        return redirect(url_for('showLogin'))
# Showing watches based on watch category


@app.route('/watchStore/<int:w1xid>/All')
def showWatches(w1xid):
    w1x_c12 = session.query(Watchname).all()
    w1xs = session.query(Watchname).filter_by(id=w1xid).one()
    w1xes = session.query(Watchlist).filter_by(watchnameid=w1xid).all()
    try:
        if login_session['username']:
            return render_template('showWatches.html', w1x_c12=w1x_c12,
                                   w1xs=w1xs, w1xes=w1xes,
                                   uname=login_session['username'])
    except:
        return render_template('showWatches.html',
                               w1x_c12=w1x_c12, w1xs=w1xs, w1xes=w1xes)
# Add New watch


@app.route('/watchStore/addWatch', methods=['POST', 'GET'])
def addWatch():
    if request.method == 'POST':
        watch = Watchname(
            name=request.form['name'],
            user_id=login_session['user_id'])
        session.add(watch)
        session.commit()
        return redirect(url_for('Watchstore'))
    else:
        return render_template('addWatchCompany.html', w1x_c12=w1x_c12)
# Edit watch Category


@app.route('/watchStore/<int:w1xid>/edit', methods=['POST', 'GET'])
def editWatchCategory(w1xid):
    editwatch = session.query(Watchname).filter_by(id=w1xid).one()
    creator = getUserInfo(editwatch.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this watch Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Watchstore'))
    if request.method == "POST":
        if request.form['name']:
            editwatch.name = request.form['name']
        session.add(editwatch)
        session.commit()
        flash("watch Category Edited Successfully")
        return redirect(url_for('Watchstore'))
    else:
        # w1x_c12 is global variable we can them in entire application
        return render_template('editWatchCategory.html',
                               w1x=editwatch, w1x_c12=w1x_c12)
# Delete watch Category


@app.route('/watchStore/<int:w1xid>/delete', methods=['POST', 'GET'])
def deleteWatchCategory(w1xid):
    w1x = session.query(Watchname).filter_by(id=w1xid).one()
    creator = getUserInfo(w1x.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this watch Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('Watchstore'))
    if request.method == "POST":
        session.delete(w1x)
        session.commit()
        flash("watch Category Deleted Successfully")
        return redirect(url_for('Watchstore'))
    else:
        return render_template('deleteWatchCategory.html', w1x=w1x, w1x_c12=w1x_c12)
# Add New watch Details


@app.route('/watchStore/addWatch/addWatchDetails/<string:w1xname>/add',
           methods=['GET', 'POST'])
def addWatchDetails(w1xname):
    w1xs = session.query(Watchname).filter_by(name=w1xname).one()
    # See if the logged in user is not the owner of watch
    creator = getUserInfo(w1xs.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new watch details"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showWatches', w1xid=w1xs.id))
    if request.method == 'POST':
        modelname = request.form['modelname']
        description = request.form['description']
        price = request.form['price']
        rating = request.form['rating']
        color = request.form['color']
        modelweight = request.form['modelweight']
        modellength = request.form['modellength']
        modelwidth = request.form['modelwidth']
        watchdetails = Watchlist(
            modelname=modelname, description=description,
            price=price,
            rating=rating,
            color=color, modelweight=modelweight,
            modellength=modellength, modelwidth=modelwidth,
            date=datetime.datetime.now(),
            watchnameid=w1xs.id,
            user_id=login_session['user_id'])
        session.add(watchdetails)
        session.commit()
        return redirect(url_for('showWatches', w1xid=w1xs.id))
    else:
        return render_template('addWatchDetails.html',
                               w1xname=w1xs.name, w1x_c12=w1x_c12)
# Edit watch details


@app.route('/watchStore/<int:w1xid>/<string:w1xename>/edit',
           methods=['GET', 'POST'])
def editWatch(w1xid, w1xename):
    w1x = session.query(Watchname).filter_by(id=w1xid).one()
    watchdetails = session.query(Watchlist).filter_by(modelname=w1xename).one()
    # See if the logged in user is not the owner of byke
    creator = getUserInfo(w1x.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this watch edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showWatches', w1xid=w1x.id))
    # POST methods
    if request.method == 'POST':
        watchdetails.modelname = request.form['modelname']
        watchdetails.description = request.form['description']
        watchdetails.price = request.form['price']
        watchdetails.rating = request.form['rating']
        watchdetails.color = request.form['color']
        watchdetails.modelweight = request.form['modelweight']
        watchdetails.modellength = request.form['modellength']
        watchdetails.modelwidth = request.form['modelwidth']
        watchdetails.date = datetime.datetime.now()
        session.add(watchdetails)
        session.commit()
        flash("Watch Edited Successfully")
        return redirect(url_for('showWatches', w1xid=w1xid))
    else:
        return render_template(
            'editWatches.html',
            w1xid=w1xid, 
            watchdetails=watchdetails, w1x_c12=w1x_c12)
# Delte Watch Edit


@app.route('/watchstore/<int:w1xid>/<string:w1xename>/delete',
           methods=['GET', 'POST'])
def deleteWatch(w1xid, w1xename):
    w1x = session.query(Watchname).filter_by(id=w1xid).one()
    watchdetails = session.query(Watchlist).filter_by(modelname=w1xename).one()
    # See if the logged in user is not the owner of byke
    creator = getUserInfo(w1x.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this watch edition",
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showWatches', w1xid=w1x.id))
    if request.method == "POST":
        session.delete(watchdetails)
        session.commit()
        flash("Deleted Watch Successfully")
        return redirect(url_for('showWatches', w1xid=w1xid))
    else:
        return render_template(
            'deleteWatches.html',
            w1xid=w1xid, watchdetails=watchdetails, w1x_c12=w1x_c12)
# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None, headers={
            'content-type': 'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(
            json.dumps(
                'Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
# Json


@app.route('/watchStore/JSON')
def allWatchesJSON():
    watchcategories = session.query(Watchname).all()
    category_dict = [c.serialize for c in watchcategories]
    for c in range(len(category_dict)):
        watches = [i.serialize for i in session.query(
                 Watchlist).filter_by(
                watchnameid=category_dict[c]["id"]).all()]
        if watches:
            category_dict[c]["watch"] = watches
    return jsonify(Watchname=category_dict)


####
@app.route('/watchStore/watchCategories/JSON')
def categoriesJSON():
    watches = session.query(Watchname).all()
    return jsonify(watchCategories=[c.serialize for c in watches])


####
@app.route('/watchStore/watches/JSON')
def itemsJSON():
    items = session.query(Watchlist).all()
    return jsonify(watches=[i.serialize for i in items])


#####
@app.route('/watchStore/<path:watch_name>/watches/JSON')
def categoryItemsJSON(watch_name):
    watchCategory = session.query(Watchname).filter_by(name=watch_name).one()
    watches = session.query(Watchlist).filter_by(watchlist=watchCategory).all()
    return jsonify(watchEdtion=[i.serialize for i in watches])


#####
@app.route('/watchStore/<path:watch_name>/<path:edition_name>/JSON')
def ItemJSON(watch_name, edition_name):
    watchCategory = session.query(Watchname).filter_by(name=watch_name).one()
    watchEdition = session.query(Watchlist).filter_by(
           name=edition_name, watchlist=watchCategory).one()
    return jsonify(watchEdition=[watchEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
