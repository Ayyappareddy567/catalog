from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, AcBrandName, AcName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///acs.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Acs Stack"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
cmr_tpk = session.query(AcBrandName).all()


# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    cmr_tpk = session.query(AcBrandName).all()
    mars = session.query(AcName).all()
    return render_template('login.html',
                           STATE=state, cmr_tpk=cmr_tpk, mars=mars)
    # return render_template('myhome.html', STATE=state
    # cmr_tpk=cmr_tpk,mars=mars)


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
    User1 = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(User1)
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

#####
# Home


@app.route('/')
@app.route('/home')
def home():
    cmr_tpk = session.query(AcBrandName).all()
    return render_template('myhome.html', cmr_tpk=cmr_tpk)

#####
# Ac Category for admins


@app.route('/AcStock')
def AcStock():
    try:
        if login_session['username']:
            name = login_session['username']
            cmr_tpk = session.query(AcBrandName).all()
            cms = session.query(AcBrandName).all()
            mars = session.query(AcName).all()
            return render_template('myhome.html', cmr_tpk=cmr_tpk,
                                   cms=cms, mars=mars, uname=name)
    except:
        return redirect(url_for('showLogin'))

######
# Showing acs based on ac category


@app.route('/AcStock/<int:cmid>/AllBrands')
def showAcs(cmid):
    cmr_tpk = session.query(AcBrandName).all()
    cms = session.query(AcBrandName).filter_by(id=cmid).one()
    mars = session.query(AcName).filter_by(acbrandnameid=cmid).all()
    try:
        if login_session['username']:
            return render_template('showAcs.html', cmr_tpk=cmr_tpk,
                                   cms=cms, mars=mars,
                                   uname=login_session['username'])
    except:
        return render_template('showAcs.html',
                               cmr_tpk=cmr_tpk, cms=cms, mars=mars)

#####
# Add New Ac


@app.route('/AcStock/addAcBrand', methods=['POST', 'GET'])
def addAcBrand():
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        brand = AcBrandName(name=request.form['name'],
                            user_id=login_session['user_id'])
        session.add(brand)
        session.commit()
        return redirect(url_for('AcStock'))
    else:
        return render_template('addAcBrand.html', cmr_tpk=cmr_tpk)

########
# Edit Ac category


@app.route('/AcStock/<int:cmid>/edit', methods=['POST', 'GET'])
def editAcCategory(cmid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    editedAc = session.query(AcBrandName).filter_by(id=cmid).one()
    creator = getUserInfo(editedAc.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Ac Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('AcStock'))
    if request.method == "POST":
        if request.form['name']:
            editedAc.name = request.form['name']
        session.add(editedAc)
        session.commit()
        flash("Ac Category Edited Successfully")
        return redirect(url_for('AcStock'))
    else:
        # cmr_tpk is global variable we can them in entire application
        return render_template('editAcCategory.html',
                               cm=editedAc, cmr_tpk=cmr_tpk)

######
# Delete Ac Category


@app.route('/AcStock/<int:cmid>/delete', methods=['POST', 'GET'])
def deleteAcCategory(cmid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    cm = session.query(AcBrandName).filter_by(id=cmid).one()
    creator = getUserInfo(cm.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Ac Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('AcStock'))
    if request.method == "POST":
        session.delete(cm)
        session.commit()
        flash("Ac Category Deleted Successfully")
        return redirect(url_for('AcStock'))
    else:
        return render_template('deleteAcCategory.html', cm=cm, cmr_tpk=cmr_tpk)

######
# Add New Ac Name Details


@app.route('/AcStock/addBrand/addAcDetails/<string:cmname>/add',
           methods=['GET', 'POST'])
def addAcDetails(cmname):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    cms = session.query(AcBrandName).filter_by(name=cmname).one()
    # See if the logged in user is not the owner of ac
    creator = getUserInfo(cms.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showAcs', cmid=cms.id))
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        color = request.form['color']
        capacity = request.form['capacity']
        rating = request.form['rating']
        price = request.form['price']
        acmodel = request.form['acmodel']
        acdetails = AcName(name=name, year=year,
                           color=color, capacity=capacity,
                           rating=rating,
                           price=price,
                           acmodel=acmodel,
                           date=datetime.datetime.now(),
                           acbrandnameid=cms.id,
                           user_id=login_session['user_id'])
        session.add(acdetails)
        session.commit()
        return redirect(url_for('showAcs', cmid=cms.id))
    else:
        return render_template('addAcDetails.html',
                               cmname=cms.name, cmr_tpk=cmr_tpk)

######
# Edit Ac details


@app.route('/AcStock/<int:cmid>/<string:marname>/edit',
           methods=['GET', 'POST'])
def editAc(cmid, marname):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    cm = session.query(AcBrandName).filter_by(id=cmid).one()
    acdetails = session.query(AcName).filter_by(name=marname).one()
    # See if the logged in user is not the owner of ac
    creator = getUserInfo(cm.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showAcs', cmid=cm.id))
    # POST methods
    if request.method == 'POST':
        acdetails.name = request.form['name']
        acdetails.year = request.form['year']
        acdetails.color = request.form['color']
        acdetails.capacity = request.form['capacity']
        acdetails.rating = request.form['rating']
        acdetails.price = request.form['price']
        acdetails.acmodel = request.form['acmodel']
        acdetails.date = datetime.datetime.now()
        session.add(acdetails)
        session.commit()
        flash("Ac Edited Successfully")
        return redirect(url_for('showAcs', cmid=cmid))
    else:
        return render_template('editAc.html',
                               cmid=cmid, acdetails=acdetails, cmr_tpk=cmr_tpk)

#####
# Delte Ac Edit


@app.route('/AcStock/<int:cmid>/<string:marname>/delete',
           methods=['GET', 'POST'])
def deleteAc(cmid, marname):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    cm = session.query(AcBrandName).filter_by(id=cmid).one()
    acdetails = session.query(AcName).filter_by(name=marname).one()
    # See if the logged in user is not the owner of ac
    creator = getUserInfo(cm.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showAcs', cmid=cm.id))
    if request.method == "POST":
        session.delete(acdetails)
        session.commit()
        flash("Deleted Ac Successfully")
        return redirect(url_for('showAcs', cmid=cmid))
    else:
        return render_template('deleteAc.html',
                               cmid=cmid, acdetails=acdetails, cmr_tpk=cmr_tpk)

####
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
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'}
                  )[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully'
                                 'disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#####
# Json


@app.route('/AcStock/JSON')
def allAcsJSON():
    accategories = session.query(AcBrandName).all()
    category_dict = [c.serialize for c in accategories]
    for c in range(len(category_dict)):
        acs = [i.serialize for i in session.query(
                 AcName).filter_by(acbrandnameid=category_dict[c]["id"]).all()]
        if acs:
            category_dict[c]["ac"] = acs
    return jsonify(AcBrandName=category_dict)

####


@app.route('/acStock/acCategories/JSON')
def categoriesJSON():
    acs = session.query(AcBrandName).all()
    return jsonify(acCategories=[c.serialize for c in acs])

####


@app.route('/acStock/acs/JSON')
def itemsJSON():
    items = session.query(AcName).all()
    return jsonify(acs=[i.serialize for i in items])

#####


@app.route('/acStock/<path:acbrandname>/acs/JSON')
def categoryitemsJSON(acbrandname):
    acBrandName = session.query(AcBrandName).filter_by(name=acbrandname).one()
    acs = session.query(AcName).filter_by(acbrandname=acBrandName).all()
    return jsonify(acBrandName=[i.serialize for i in acs])

#####


@app.route('/acStock/<path:acbrandname>/<path:edition_name>/JSON')
def ItemJSON(acbrandname, edition_name):
    acBrandName = session.query(AcBrandName).filter_by(name=acbrandname).one()
    acEdition = session.query(AcName).filter_by(
           name=edition_name, acbrandname=acBrandName).one()
    return jsonify(acEdition=[acEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
