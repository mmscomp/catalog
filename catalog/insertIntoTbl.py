from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app1DB import Base, Sports, Entertainment, Diary, Education, Business, User
engine = create_engine('sqlite:///app1withusers.db')

# Bind the engine to the metadata of the Base class so that the

# declaratives can be accessed through a DBSession instance

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Sports.__table__.create(engine)

# Create dummy user
'''
User1 = User(name="Robo Copa", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User1 = User(name="Manoj", email="manojshrestha035@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170400x400.png')
session.add(User1)
session.commit()

# Menu for UrbanBurger

#catalog1 = Catalog(name="")
#session.add(catalog1)
#session.commit()
#menuItem2 = MenuItem(user_id=1, name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                     price="$7.50", course="Entree", restaurant=restaurant1)


#Diary
diary1 = Diary(user_id=1, name="Manoj Shrestha", title="A good start", description = "After a long pause, I started to code again", date="2017-8-23")

#education
edu1 = Education(user_id=1, name="Natural Science", description="Study of laws of nature and the stuff around us as well as stuff far awya", favorite="Physics")
session.add(edu1)
session.commit()

edu2 = Education(user_id = 1, name="Biological Science", description="Study of living things  ranging from miniscule microbes to giant mammals", favorite="Zoology")
session.add(edu2)
session.commit()
edu3 = Education(user_id=1, name="Political Science", description="Study of goverance of a state or a country", favorite="Democracy")
session.add(edu3)
session.commit()

edu4 = Education(user_id=1, name="Computer Science", description="Study of computers involving hardware as well as software", favorite="Python programming")
session.add(edu4)
session.commit()
'''
'''
#business
bus1 = Business(user_id=1, name="Hospitality", description="Accomodating tavellers from their travel needs to travel destinations", favorite="Hotel business")
session.add(bus1)
session.commit()
#Entertainment
Entertain1 = Entertainment(user_id=1, name="Movies",description="Drama, humor, or actual depiction of situations about one - two hours best viewed on Cinema Halls", favorite="Predator 1 - a sci - fi movie")
session.add(Entertain1)
session.commit()
Entertain2 = Entertainment(user_id=1, name="TV", description="TV programs are watched at homes, which range form live news to movies", favorite="Two and Half Men")
session.add(Entertain2)
session.commit()
Entertain3 = Entertainment(user_id=1, name="Amusement Parks",description="DareDevils events especially rollercoasters", favorite="Cidar Point in OHIO")
session.add(Entertain3)
session.commit()
Entertain4 = Entertainment(user_id=1, name="Traveling", description="Taking a pause from daily routine to travel to a fra away place", favorite="Europe")
session.add(Entertain4)
session.commit()
Entertain5 = Entertainment(user_id=1, name="Picnic", description="Gathering of friends and families in an outdoor setting", favorite="ZOO")
session.add(Entertain5)
session.commit()
'''
#Sports Item

Sports1 = Sports( user_id=1, name="Soccer", description="Most popular sports on the planet -- win by scoring more goals that your opponent team", favorite="World Cup") 
#Sports1 = Sports(user_id=1, name="Soccer", favorite="World Cup")
session.add(Sports1)
session.commit()

'''
Sports2 = Sports(name="Basketball")#, user_id=1)
session.add(Sports2)
session.commit()
Sports3 = Sports(name="Football")#, user_id=1)
session.add(Sports3)
session.commit()
Sports4 = Sports(name="Boxing")#, user_id=1)
session.add(Sports4)
session.commit()
Sports5 = Sports(name="Wrestling")#, user_id=1)
session.add(Sports5)
session.commit()
Sports6 = Sports(name="Athletics")#, user_id=1)
session.add(Sports6)
session.commit()

#SportsItem = SportsItem(name='World Cup', sports_id=1, user_id=2)
#session.add(SportsItem)
#session.commit()
SportsItem1 = SportsItem(name='Intro', sports_id=6, user_id=1)
session.add(SportsItem1)
session.commit()
SportsItem2 = SportsItem(name='World Championship', sports_id=6, user_id=2)
session.add(SportsItem2)
session.commit()
SportsItem3 = SportsItem(name='Olympics Athletics', sports_id=6, user_id=2)
session.add(SportsItem3)
session.commit()
'''



