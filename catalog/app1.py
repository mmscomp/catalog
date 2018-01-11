import string
import random
import json
import httplib2
import requests

from flask import Flask, request, redirect, url_for, jsonify,\
                   render_template, flash
from sqlalchemy import create_engine, asc

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from app1DB import engine, Base, User,  Sports, Entertainment,\
                   Education, Business, Diary, Read, PrivateDiary

from oauth2client.client import flow_from_clientsecrets

from oauth2client.client import FlowExchangeError


from flask import session as login_session

from flask import make_response

app = Flask(__name__)

# Create database session
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(

    open('./client_secrets.json', 'r').read())['web']['client_id']
print 32, CLIENT_ID
APPLICATION_NAME = "Catalog"
# Create anti-forgery state token


@app.route('/login')
def showLogin():

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)

                    for x in xrange(32))

    login_session['state'] = state

    # return "The current session state is %s" % login_session['state']

    return render_template('login.html', STATE=state)


@app.route('/fbconnect', methods=['POST'])
def fbconnect():

    if request.args.get('state') != login_session['state']:

        response = make_response(json.dumps('Invalid state parameter.'), 401)

        response.headers['Content-Type'] = 'application/json'

        return response

    access_token = request.data

    print "access token received %s " % access_token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    print 74, access_token
    app_secret = json.loads(

        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    print 78, app_id, app_secret, access_token
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=' + \
          'fb_exchange_token&client_id="%s"&client_secret="%s"&' +\
          'fb_exchange_token="%s"' % (app_id, app_secret, access_token)
    print 83, '\n\n\n', url
    h = httplib2.Http()

    result = h.request(url, 'GET')[1]

    print 81, '\n', result

    # Use token to get user info from API

    userinfo_url = "https://graph.facebook.com/v2.4/me"

    # strip expire tag from access token

    token = result.split("&")[0]  # (",")[0] +"}"
    print 90, '\n', token
    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    print 92, '\n', url
    h = httplib2.Http()

    result = h.request(url, 'GET')[1]

    print "url sent for API access:%s" % url

    print "API JSON result: %s" % result

    data = json.loads(result)
    print 136, data
    login_session['provider'] = 'facebook'

    login_session['username'] = data["name"]

    login_session['email'] = data["email"]

    login_session['facebook_id'] = data["id"]

    # Store token
    stored_token = token.split("=")[1]

    login_session['access_token'] = stored_token

    # Get user picture

    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect' + \
          '=0&height=200&width=200' % token

    h = httplib2.Http()

    result = h.request(url, 'GET')[1]

    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]
    # see if user exists

    user_id = getUserID(login_session['email'])

    if not user_id:

        user_id = createUser(login_session)
    print 178, user_id

    login_session['user_id'] = user_id

    output = ''

    output += '<h1>Welcome, '

    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'

    output += login_session['picture']

    output += ' "style = "width: 300px;" + \
                "height: 300px; border-radius:" + \
                "150px; -webkit-border-radius: 150px;" + \
                " -moz-border-radius:"150px;" "> '

    flash("Now logged in as %s" % login_session['username'])

    return output


@app.route('/fbdisconnect')
def fbdisconnect():

    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout

    access_token = login_session['access_token']

    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (
        facebook_id, access_token)

    h = httplib2.Http()

    result = h.request(url, 'DELETE')[1]

    return "you have been logged out"


@app.route('/gconnect', methods=['POST'])
def gconnect():

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
        print '000.', type(credentials)
    except FlowExchangeError:

        response = make_response(

            json.dumps('Failed to upgrade the authorization code.'), 401)

        response.headers['Content-Type'] = 'application/json'

        return response

    # Check that the access token is valid.

    access_token = credentials.access_token
    print 0., credentials

    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
           access_token)

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

        print "Token's client ID does not match app's."

        response.headers['Content-Type'] = 'application/json'

        return response

    stored_credentials = login_session.get('credentials')

    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and gplus_id == stored_gplus_id:
        # added new line code

        login_session['credentials'] = credentials.access_token # change from credentials
        response = make_response(json.dumps('Current user is already' +
                                            ' connected.'), 200)

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

    login_session['provider'] = 'google'
    login_session['username'] = data['name']

    login_session['picture'] = data['picture']

    login_session['email'] = data['email']

    # ADD PROVIDER TO LOGIN SESSION
    # see if user exists, if it doesn't make a new one

    user_id = getUserID(data["email"])
    print 383, user_id
    if not user_id:

        user_id = createUser(login_session)

    print 388, user_id
    login_session['user_id'] = user_id
    output = ''

    output += '<h1>Welcome, '

    output += login_session['username']

    output += '!</h1>'

    output += '<img src="'

    output += login_session['picture']

    output += ' " style = "width: 300px; height: 300px;" + \
                "border-radius: 150px; "-webkit-border-radius:" + \
                " 150px;-moz-border-radius: 150px;" "> '

    flash("you are now logged in as %s" % login_session['username'])

    print "done!"

    return output


def createUser(login_session):

    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    print 372, login_session['username'], login_session['email']
    l = [login_session['username'],
         login_session['email'], login_session['picture']]
    session.add(newUser)

    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    print 379, user
    return user


def getUserInfo(user_id):

    user = session.query(User).filter_by(id=user_id).one()
    print 395, user
    return user


def getUserID(email):

    try:

        user = session.query(User).filter_by(email=email).one()
        return user.id

    except:

        return None


# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():

    # Only disconnect a connected user.

    credentials = login_session.get('credentials')

    if credentials is None:

        response = make_response(

            json.dumps('Current user not connected.'), 401)

        response.headers['Content-Type'] = 'application/json'

        return response

    access_token = credentials    #.access_token

    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token

    h = httplib2.Http()

    result = h.request(url, 'GET')[0]
    if result['status'] != '200':

        # For whatever reason, the given token was invalid.

        response = make_response(

            json.dumps('Failed to revoke token for given user.'), 400)

        response.headers['Content-Type'] = 'application/json'

        return response


# JSON APIs to view Sports Information
@app.route('/catalog/sports/JSON')
def sportsJSON():

    sports = session.query(Sports).all()
    return jsonify(SportsItems=[i.serialize for i in sports])


@app.route('/catalog/entertainment/JSON')
def entertainmentJSON():
    entertainment = session.query(Entertainment).all()
    return jsonify(EntertainmentItems=[i.serialize for i in entertainment])


@app.route('/catalog/business/JSON')
def businessJSON():
    business = session.query(Business).all()
    return jsonify(BusinessItems=[i.serialize for i in business])


@app.route('/catalog/education/JSON')
def educationJSON():
    education = session.query(Education).all()
    return jsonify(EducationItems=[i.serialize for i in education])


@app.route('/catalog/diary/JSON')
def diaryJSON():
    diary = session.query(Diary).all()
    return jsonify(DiaryItems=[i.serialize for i in diary])


@app.route('/register', methods=['GET', 'POST'])
def register():
    return "complicated!"


@app.route('/')
def showWitch():
    return render_template('index.html')

@app.route('/catalog/')
def showCatalog():
    #    catalog = session.query(Catalog).order_by(asc(Catalog.name)).all()
    email = login_session.get('email')
    if 'username' in login_session:
        id = login_session['user_id']
    if 'username' not in login_session:
        return render_template('catalog.html')
    else:
        return render_template('catalog.html', id=id)

# Sports
@app.route('/catalog/sports/')
def showSports():
    sports = session.query(Sports).order_by(asc(Sports.name))
    print '888. ', sports
    if 'username' not in login_session:
        return render_template('publicsports.html', sports=sports)
    else:
        return render_template('sports.html', sports=sports,
                               id=login_session['user_id'])


@app.route('/catalog/sports/<name>')
def showSportsItem(name):
    sports = session.query(Sports).order_by(asc(Sports.name))
    sportsItemUser = session.query(Sports).filter_by(name=name).one()
    creator = getUserInfo(sportsItemUser.user_id)
    sportsItem = session.query(Sports).filter_by(name=name).all()
    if 'username' not in login_session or \
       creator.id != login_session['user_id']:
        return render_template('publicsportsitem.html',
                               sports=sports, sportsItem=sportsItem)
    else:
        return render_template('sportsitem.html', sports=sports,
                               sportsItem=sportsItem,
                               creator_id=creator.id,
                               id=login_session['user_id'])


#Sports type
@app.route('/catalog/sports/<name>/<e1>')
def showSportsItemType(name,e1):
    sports = session.query(
        Sports).order_by(asc(Sports.name))
    sportsOne = session.query(Sports).filter_by(name=name).one()
    creator = getUserInfo(sportsOne.user_id)
    sportsItem = session.query(Sports).filter_by(
                        name=name).all()
   
    if 'username' not in login_session or creator.id != \
       login_session['user_id']:
        return render_template('publicsportsitemtype.html',
                               sports=sports,
                               sportsItem=sportsItem,
                               name=name, type1=e1)
    else:
        return render_template('sportsitemtype.html',
                               sports=sports,
                               sportsItem=sportsItem,
                               creator_id=creator.id,
                               id=login_session['user_id'],
                               name=name, type1=e1)

# Entertainment
@app.route('/catalog/entertainment/')
def showEntertainment():
    entertainment = session.query(
        Entertainment).order_by(asc(Entertainment.name))
    print 489, entertainment
    if 'username' not in login_session:
        return render_template('publicentertainment.html',
                               entertainment=entertainment)
    else:
        return render_template('entertainment.html',
                               entertainment=entertainment,
                               id=login_session['user_id'])



@app.route('/catalog/entertainment/<name>')
def showEntertainmentItem(name):
    entertainment = session.query(
        Entertainment).order_by(asc(Entertainment.name))
    print 502, entertainment
    entertain = session.query(Entertainment).filter_by(name=name).one()
    print 504, getUserInfo(entertain.user_id)
    creator = getUserInfo(entertain.user_id)
    entertainmentItem = session.query(Entertainment).filter_by(
                        name=name).all()
    print 1000, creator, entertainmentItem
    if 'username' not in login_session or creator.id != \
       login_session['user_id']:
        return render_template('publicentertainmentitem.html',
                               entertainment=entertainment,
                               entertainmentItem=entertainmentItem)
    else:
        return render_template('entertainmentitem.html',
                               entertainment=entertainment,
                               entertainmentItem=entertainmentItem,
                               creator_id=creator.id,
                               id=login_session['user_id'])

#
@app.route('/catalog/entertainment/<name>/<e1>')
def showEntertainmentItemType(name,e1):
    entertainment = session.query(
        Entertainment).order_by(asc(Entertainment.name))
    print 502, entertainment
    entertain = session.query(Entertainment).filter_by(name=name).one()
    print 504, getUserInfo(entertain.user_id)
    creator = getUserInfo(entertain.user_id)
    entertainmentItem = session.query(Entertainment).filter_by(
                        name=name).all()
    print 1000, creator, entertainmentItem
    if 'username' not in login_session or creator.id != \
       login_session['user_id']:
        return render_template('publicentertainmentitemtype.html',
                               entertainment=entertainment,
                               entertainmentItem=entertainmentItem,
                               name=name, type1=e1)
    else:
        return render_template('entertainmentitemtype.html',
                               entertainment=entertainment,
                               entertainmentItem=entertainmentItem,
                               creator_id=creator.id,
                               id=login_session['user_id'],
                               name=name, type1=e1)


@app.route('/catalog/business/')
def showBusiness():
    business = session.query(Business).order_by(asc(Business.name))
    print 489, business
    if 'username' not in login_session:
        return render_template('publicbusiness.html', business=business)
    else:
        return render_template('business.html', business=business,
                               id=login_session['user_id'])



@app.route('/catalog/business/<name>')
def showBusinessItem(name):
    business = session.query(Business)
    businessItemUser = session.query(Business).filter_by(name=name).one()
    creator = getUserInfo(businessItemUser.user_id)
    businessItem = session.query(Business).filter_by(name=name).all()
    print 1000, businessItem
    if 'username' not in login_session or creator.id != \
       login_session['user_id']:
        return render_template('publicbusinessitem.html',
                               business=business,
                               businessItem=businessItem)
    else:
        return render_template('businessitem.html', business=business,
                               businessItem=businessItem,
                               creator_id=creator.id,
                               id=login_session['user_id'])



@app.route('/catalog/education/')
def showEducation():
    education = session.query(Education).order_by(asc(Education.name))
    if 'username' not in login_session:
        return render_template('publiceducation.html', education=education)
    else:
        return render_template('education.html', education=education,
                               id=login_session['user_id'])


@app.route('/catalog/education/<name>')
def showEducationItem(name):
    education = session.query(Education).order_by(asc(Education.name))
    educationItemUser = session.query(Education).filter_by(name=name).one()
    creator = getUserInfo(educationItemUser.user_id)
    educationItem = session.query(Education).filter_by(name=name).all()

    if 'username' not in login_session or creator.id != \
       login_session['user_id']:
        return render_template('publiceducationitem.html',
                               education=education,
                               educationItem=educationItem)
    else:
        return render_template('educationitem.html',
                               education=education,
                               educationItem=educationItem,
                               creator_id=creator.id,
                               id=login_session['user_id'])


#
@app.route('/catalog/education/<name>/<e1>')
def showEducationItemType(name,e1):
    education = session.query(
        Education).order_by(asc(Education.name))
    educationOne = session.query(Education).filter_by(name=name).one()
    creator = getUserInfo(educationOne.user_id)
    educationItem = session.query(Education).filter_by(
                        name=name).all()

    if 'username' not in login_session or creator.id != \
       login_session['user_id']:
        return render_template('publiceducationitemtype.html',
                               education=education,
                               educationItem=educationItem,
                               name=name, type1=e1)
    else:
        return render_template('educationitemtype.html',
                               education=education,
                               educationItem=educationItem,
                               creator_id=creator.id,
                               id=login_session['user_id'],
                               name=name, type1=e1)


@app.route('/catalog/read/')
def showRead():
    read = session.query(Read).order_by(asc(Read.name))
    if 'username' not in login_session:
        return render_template('publicread.html', read=read)
    else:
        return render_template('read.html', read=read,
                               id=login_session['user_id'])



@app.route('/catalog/read/<name>')
def showReadItem(name):
    read = session.query(Read).order_by(asc(Read.name))
    readItemUser = session.query(Read).filter_by(name=name).one()
    creator = getUserInfo(readItemUser.user_id)
    readItem = session.query(Read).filter_by(name=name).all()

    if 'username' not in login_session or creator.id != \
       login_session['user_id']:
        return render_template('publicreaditem.html',
                               read=read,
                               readItem=readItem)
    else:
        return render_template('readitem.html',
                               read=read,
                               readItem=readItem,
                               creator_id=creator.id,
                               id=login_session['user_id'])




@app.route('/catalog/diary/')
def showDiary():
    diary = session.query(Diary).order_by(asc(Diary.name))
    if 'username' not in login_session:
        return render_template('publicdiary.html', diary=diary)
    else:
        return render_template('diary.html', diary=diary,
                               id=login_session['user_id'])


@app.route('/catalog/diary/<name>')
def showDiaryItem(name):
    diary = session.query(Diary).order_by(asc(Diary.name))
    diaryItemUser = session.query(Diary).filter_by(name=name).one()
    creator = getUserInfo(diaryItemUser.user_id)
    diaryItem = session.query(Diary).filter_by(name=name).all()

    if 'username' not in login_session or creator.id != \
       login_session['user_id']:
        return render_template('publicdiaryitem.html',
                               diary=diary, diaryItem=diaryItem)
    else:
        return render_template('diaryitem.html', diary=diary,
                               diaryItem=diaryItem,
                               creator_id=creator.id)

@app.route('/catalog/privatediary/<id>')
def showPrivateDiary(id):
    diary = session.query(Diary).order_by(asc(Diary.name))
    pdiary = session.query(PrivateDiary).order_by(asc(PrivateDiary.name)).filter_by(user_id=id).all()
   # diaryItemUser = session.query(PrivateDiary).filter_by(name=name).one()
    if len(pdiary) != 0:
        creator = getUserInfo(pdiary[0].user_id)
    
    if 'username' not in login_session:
        return render_template('publicdiary.html', diary=diary)
    elif  len(pdiary) > 0 and login_session['user_id'] != creator.id:
        return render_template('diary.html', diary=diary)
    else:
        return render_template('privateDiary.html', pdiary=pdiary, id=id)

@app.route('/catalog/privatediaryitem/<id>/<name>')
def showPrivateDiaryItem(id, name):
    print 2000, id
    diary = session.query(Diary).order_by(asc(Diary.name))
    pdiary = session.query(PrivateDiary).order_by(asc(PrivateDiary.name)).filter_by(user_id=id).all()
    
    
    creator = getUserInfo(pdiary[0].user_id)
    diaryItem = session.query(Diary).filter_by(name=name).all()
    pdiaryItem = session.query(PrivateDiary).filter_by(name=name).all()

    if 'username' not in login_session or login_session['user_id'] \
        != creator.id:
        return render_template('publicdiaryitem.html',
                               diary=diary, diaryItem=diaryItem)
    elif 'username'  in login_session and login_session['user_id'] \
         != creator.id:
        return render_template('diaryitem.html', diary=diary,
                               diaryItem=diaryItem)
    else:
        return render_template('privatediaryitem.html', pdiary=pdiary,
                               pdiaryItem=pdiaryItem,
                               id=login_session['user_id'])

# Maps of Places
@app.route('/catalog/publicplace.html/')
def showPlace():
#    read = session.query(Read).order_by(asc(Read.name))
#    if 'username' not in login_session:
    return render_template('publicplace.html')

# Create, edit, delete category

# Sports category
@app.route('/catalog/sports/new/', methods=['GET', 'POST'])
def newSports():

    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newSports = Sports(name=request.form['name'],
                           description=request.form['description'],
                           favorite=request.form['favorite'],
                           user_id=login_session['user_id'])
        session.add(newSports)
        session.commit()
        flash('New Sports category %s Successfully Created' % newSports.name)
        return redirect(url_for('showSports'))
    else:
        return render_template('newsports.html')


@app.route('/catalog/sports/edit/<name>', methods=['GET', 'POST'])
def editSports(name):
    editedSports = session.query(
        Sports).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedSports.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not" + \
               "authorized to edit this category. Please create your" + \
               "own category in order to edit.');}</script><body" + \
               "onload='myFunction()'>"

    if request.method == 'POST':

        if request.form['name']:
            editedSports.name = request.form['name']
        if request.form['description']:
            editedSports.description = request.form['description']
        if request.form['favorite']:
            editedSports.favorite = request.form['favorite']
            session.add(editedSports)
            session.commit()
            flash('Sports Successfully Edited %s' % editedSports.name)
            return redirect(url_for('showSports'))
    else:
        return render_template('editSports.html', sports=editedSports)

# Delete a sports category


@app.route('/category/sports/<name>/delete/', methods=['GET', 'POST'])
def deleteSports(name):
    sportsToDelete = session.query(
        Sports).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if sportsToDelete.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not" + \
               "authorized to delete this category. Please create" + \
               "your own category in order to delete.');}</script>" + \
               "<body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(sportsToDelete)
        flash('%s Successfully Deleted' % sportsToDelete.name)
        session.commit()
        return redirect(url_for('showsports', name=name))
    else:
        return render_template('deleteSports.html', sports=sportsToDelete)

# Entertainment category


@app.route('/catalog/entertainment/new/', methods=['GET', 'POST'])
def newEntertainment():

    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newEntertainment = Entertainment(
                                name=request.form['name'],
                                description=request.form['description'],
                                favorite=request.form['favorite'],
                                user_id=login_session['user_id'])
        session.add(newEntertainment)
        session.commit()
        flash('New Entertainment element Successfully Created')
        return redirect(url_for('showEntertainment'))
    else:
        return render_template('newentertainment.html')


@app.route('/catalog/entertainment/edit/<name>', methods=['GET', 'POST'])
def editEntertainment(name):
    editedEntertainment = session.query(
        Entertainment).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedEntertainment.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not" + \
               " authorized to edit this category. Please create your" + \
               " own category in order to edit.');}</script><body" + \
               "onload='myFunction()''>"

    if request.method == 'POST':

        if request.form['name']:
            editedEntertainment.name = request.form['name']
        if request.form['description']:
            editedEntertainment.description = request.form['description']
        if request.form['favorite']:
            editedEntertainment.favorite = request.form['favorite']
            session.add(editedEntertainment)
            session.commit()
            flash('Entertainment Successfully Edited %s' %
                  editedEntertainment.name)
            return redirect(url_for('showEntertainment'))
    else:
        return render_template('editEntertainment.html',
                               entertainment=editedEntertainment)


# Delete an Entertainment category
@app.route('/category/entertainment/<name>/delete/', methods=['GET', 'POST'])
def deleteEntertainment(name):
    enterToDelete = session.query(
        Entertainment).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if enterToDelete.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not" \
               + " authorized to delete this category. Please create your" \
                + " own category in order to delete.');}</script><body" \
                + " onload='myFunction()'>"

    if request.method == 'POST':
        session.delete(enterToDelete)
        flash('%s Successfully Deleted' % enterToDelete.name)
        session.commit()
        return redirect(url_for('showEntertainment', name=name))
    else:
        return render_template('deleteEntertainment.html',
                               entertain=enterToDelete)


# Business category
@app.route('/catalog/business/new/', methods=['GET', 'POST'])
def newBusiness():

    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newBusiness = Business(name=request.form['name'],
                               description=request.form['description'],
                               favorite=request.form['favorite'],
                               user_id=login_session['user_id'])
        session.add(newBusiness)
        session.commit()
        flash('New Business category Successfully Created')
        return redirect(url_for('showBusiness'))
    else:
        return render_template('newBusiness.html')


@app.route('/catalog/business/edit/<name>', methods=['GET', 'POST'])
def editBusiness(name):
    editedBusiness = session.query(
        Business).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedBusiness.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not" + \
               " authorized to edit this category. Please create" + \
               " your own category in order to edit.');}</script><body" + \
               " onload='myFunction()'>"

    if request.method == 'POST':

        if request.form['name']:
            editedBusiness.name = request.form['name']
        if request.form['description']:
            editedBusiness.descriptioni = request.form['description']
        if request.form['favorite']:
            editedBusiness.favorite = request.form['favorite']
            session.add(editedBusiness)
            session.commit()
            flash('Business category Successfully Edited %s' %
                  editedBusiness.name)
            return redirect(url_for('showBusiness'))
    else:
        return render_template('editBusiness.html', business=editedBusiness)


# Delete a business category
@app.route('/category/<name>/delete/', methods=['GET', 'POST'])
def deleteBusiness(name):
    bussinessToDelete = session.query(
        Business).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if businessToDelete.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not" + \
               "authorized to delete this category. Please create" + \
               " your own category in order to delete.')" + \
               ";}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(businessToDelete)
        flash('%s Successfully Deleted' % businessToDelete.name)
        session.commit()
        return redirect(url_for('showBusiness', name=name))
    else:
        return render_template('deleteBusiness.html',
                               entertain=businessToDelete)


# Education category
@app.route('/catalog/education/new/', methods=['GET', 'POST'])
def newEducation():

    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newEducation = Education(name=request.form['name'],
                                 description=request.form['description'],
                                 favorite=request.form['favorite'],
                                 user_id=login_session['user_id'])
        session.add(newEducation)
        session.commit()
        flash('New Education Category Successfully Created')
        return redirect(url_for('showEducation'))
    else:
        return render_template('newEducation.html')


@app.route('/catalog/education/edit/<name>', methods=['GET', 'POST'])
def editEducation(name):
    editedEducation = session.query(
        Education).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedEducation.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not" + \
               " authorized to edit this category. Please create your" + \
               "own category in order to edit.');}</script><body" + \
               "onload='myFunction()'>"

    if request.method == 'POST':

        if request.form['name']:
            editedEducation.name = request.form['name']
        if request.form['description']:
            editedEducation.description = request.form['description']
        if request.form['favorite']:
            editedEducation.favorite = request.form['favorite']
            session.add(editedEducation)
            session.commit()
            flash('Education Successfully Edited %s' % editedEducation.name)
            return redirect(url_for('showEducation'))
    else:
        return render_template('editEducation.html',
                               education=editedEducation)


# Delete an Education category
@app.route('/category/<name>/delete/', methods=['GET', 'POST'])
def deleteEducation(name):
    eduToDelete = session.query(
        Education).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if eduToDelete.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert" + \
               "('You are not authorized to delete this category." + \
               " Please create your own category in order to delete.'" + \
               ");}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(eduToDelete)
        flash('%s Successfully Deleted' % eduToDelete.name)
        session.commit()
        return redirect(url_for('showEducation', name=name))
    else:
        return render_template('deleteEducation.html',
                               education=eduToDelete)


# Read category
@app.route('/catalog/read/new/', methods=['GET', 'POST'])
def newRead():

    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newRead = Read(name=request.form['name'],
                                 description=request.form['description'],
                                 favorite=request.form['favorite'],
                                 user_id=login_session['user_id'])
        session.add(newRead)
        session.commit()
        flash('New Read Category Successfully Created')
        return redirect(url_for('showRead'))
    else:
        return render_template('newRead.html')

# Edit a Read category
@app.route('/catalog/read/edit/<name>', methods=['GET', 'POST'])
def editRead(name):
    editedRead = session.query(
        Read).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedRead.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not" + \
               " authorized to edit this category. Please create your" + \
               "own category in order to edit.');}</script><body" + \
               "onload='myFunction()'>"

    if request.method == 'POST':

        if request.form['name']:
            editedRead.name = request.form['name']
        if request.form['description']:
            editedRead.description = request.form['description']
        if request.form['favorite']:
            editedRead.favorite = request.form['favorite']
            session.add(editedRead)
            session.commit()
            flash('Read Successfully Edited %s' % editedRead.name)
            return redirect(url_for('showRead'))
    else:
        return render_template('editRead.html',
                               read=editedRead)

# Delete a read category
@app.route('/category/<name>/delete/', methods=['GET', 'POST'])
def deleteRead(name):
    readToDelete = session.query(
        Read).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if readToDelete.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert" + \
               "('You are not authorized to delete this category." + \
               " Please create your own category in order to delete.'" + \
               ");}</script><body onload='myFunction()''>"

    if request.method == 'POST':
        session.delete(readToDelete)
        flash('%s Successfully Deleted' % readToDelete.name)
        session.commit()
        return redirect(url_for('showRead', name=name))
    else:
        return render_template('deleteRead.html',
                               read=readToDelete)


# Diary category
@app.route('/catalog/diary/new/', methods=['GET', 'POST'])
def newDiary():

    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newDiary = Diary(name=request.form['name'],
                         description=request.form['description'],
                         title=request.form['title'],
                         date=request.form['date'],
                         user_id=login_session['user_id'])
        session.add(newDiary)
        session.commit()
        flash('New Diary created. %s' % newDiary.name)
        return redirect(url_for('showDiary'))
    else:
        return render_template('newDiary.html')

#
@app.route('/catalog/diary/edit/<name>', methods=['GET', 'POST'])
def editDiary(name):
    editedDiary = session.query(
        Diary).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedDiary.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not authorized" \
               + " to edit this category. Please create your own category in" \
               + " order to edit.');}</script><body onload='myFunction()'>"

    if request.method == 'POST':

        if request.form['name']:
            editedDiary.name = request.form['name']
        if request.form['description']:
            editedDiary.description = request.form['description']
        if request.form['favorite']:
            editedDiary.favorite = request.form['favorite']
            session.add(editedDiary)
            session.commit()
            flash('Diary element Successfully Edited %s' % editedDiary.name)
            return redirect(url_for('showDiary'))
    else:
        return render_template('editDiary.html', diary=editedDiary)

# Delete a diary category
@app.route('/category/diary/<name>/delete/', methods=['GET', 'POST'])
def deleteDiary(name):
    diaryToDelete = session.query(
        Diary).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if diaryToDelete.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not " + \
               " authorized to delete this category. Please create" + \
               " your own category in" + \
               " order to delete.');}</script><body onload='myFunction()'>"

    if request.method == 'POST':
        session.delete(diaryToDelete)
        flash('%s Successfully Deleted' % diaryToDelete.name)
        session.commit()
        return redirect(url_for('showDiary', name=name))
    else:
        return render_template('deleteDiary.html', diary=diaryToDelete)


# Private diary category
@app.route('/catalog/privatediary/new/', methods=['GET', 'POST'])
def newPrivateDiary():
    print 'username'
    if 'username' not in login_session:
        return redirect('/login')
    oldDiary = session.query(PrivateDiary).filter_by(user_id = \
                                          login_session['user_id']).all()
#    print '1000', oldDiary[0].name 
    if request.method == 'POST':
        name=request.form['name']
        for data in oldDiary:
            if name== data.name:
                flash('Name already taken; choose a different name')
                return render_template('newPrivateDiary.html', id = login_session['user_id'] )
             
        newDiary = PrivateDiary(name=name,
                         description=request.form['description'],
                         title=request.form['title'],
                         date=request.form['date'],
                         user_id=login_session['user_id'])
        session.add(newDiary)
        session.commit()
        print 1073, newDiary.name
        flash('New Diary created. %s' % newDiary.name)
        return redirect(url_for('showPrivateDiary', name=newDiary.name,
                                id=newDiary.user_id))
    else:
        return render_template('newPrivateDiary.html', id = login_session['user_id'] )

@app.route('/catalog/privatediary/edit/<name>', methods=['GET', 'POST'])
def editPrivateDiary(name):
    editedDiary = session.query(
        PrivateDiary).filter_by(name=name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedDiary.user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not authorized" \
               + " to edit this category. Please create your own category in" \
               + " order to edit.');}</script><body onload='myFunction()'>"

    if request.method == 'POST':

        if request.form['name']:
            editedDiary.name = request.form['name']
        if request.form['description']:
            editedDiary.description = request.form['description']
        if request.form['favorite']:
            editedDiary.favorite = request.form['favorite']
            session.add(editedDiary)
            session.commit()
            flash('Diary element Successfully Edited %s' % editedDiary.name)
            return redirect(url_for('showDiary'))
    else:
        return render_template('editDiary.html', diary=editedDiary)


# Delete a diary category
@app.route('/category/privatediary/<name>/delete/', methods=['GET', 'POST'])
def deletePrivateDiary(name):
    diaryToDelete = session.query(
        PrivateDiary).filter_by(name=name).all()
    if 'username' not in login_session:
        return redirect('/login')
    id = diaryToDelete[0].user_id
    if diaryToDelete[0].user_id != login_session['user_id']:

        return "<script>function myFunction() {alert('You are not " + \
               " authorized to delete this category. Please create" + \
               " your own category in" + \
               " order to delete.');}</script><body onload='myFunction()'>"

    if request.method == 'POST':
        session.delete(diaryToDelete[0])
        flash('%s Successfully Deleted' % diaryToDelete[0].name)
        session.commit()
        return redirect(url_for('showPrivateDiary', id=id, name=name))
    else:
        return render_template('deletePrivateDiary.html', id=id, diary=diaryToDelete)

@app.route('/blog')
def showBlog():
    return render_template('publicblog.html')

# disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
        #    del login_session['credentials']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showCatalog'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showCatalog'))


if __name__ == '__main__':
    app.secret_key = 'JamesBond007'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
