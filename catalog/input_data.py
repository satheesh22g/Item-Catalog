from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import State, Base, TouristPlace, User

engine = create_engine('sqlite:///tourism.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()

# Create a user
User1 = User(
    name="satheesh g",
    email="satheeshgajula22@gmail.com",
    picture='https://lh5.googleusercontent.com/-dUqqq_sfAeY/'
            'AAAAAAAAAAI/AAAAAAAAInQ/E3m3jNiJbhs/photo.jpg')
session.add(User1)
session.commit()


# create a State Andrapradesh
state1 = State(name="Andra Pradesh", user_id=1)
session.add(state1)
session.commit()


# create Tourist places in Andhrapradesh
tourist_place1 = TouristPlace(
    user_id=1,
    name="Araku Valley",
    description="is a scenic hill station in the"
                "Vishakhapatnam district of Andhra Pradesh",
    distance="432 km from Vijayawada",
    language="Telugu",
    state=state1)
session.add(tourist_place1)
session.commit()


tourist_place2 = TouristPlace(
    user_id=1,
    name="Srisailam",
    description="Srisailam is one of the twelve Jyotirlingas of"
                "Lord Shiva situated on the banks of River Krishna",
    distance="229 km from Hyderabad",
    language="Telugu",
    state=state1)
session.add(tourist_place2)
session.commit()


tourist_place3 = TouristPlace(
    user_id=1,
    name="Tirupati",
    description="Tirupati is a pilgrimage city in the extreme"
                "southeast of Andhra Pradesh in Chittoor district",
    distance="134 km from Chennai",
    language="Telugu",
    state=state1)
session.add(tourist_place3)
session.commit()


tourist_place4 = TouristPlace(
    user_id=1,
    name="Lepakshi",
    description="Lepakshi is a small village highlighting the"
                "legacy of Vijayanagara Dynasty in Anantapur district",
    distance="124 km from Bangalore",
    language="Telugu",
    state=state1)
session.add(tourist_place4)
session.commit()


# create a State Karnataka
state2 = State(user_id=1, name="Karnataka")
session.add(state2)
session.commit()


# create tourist palces in Karanataka
tourist_place1 = TouristPlace(
    user_id=1,
    name="Bandipur National Park",
    description="is one of the well preserved National Parks in India",
    distance="80 km from Mysore",
    language="Kannada",
    state=state2)
session.add(tourist_place1)
session.commit()


tourist_place2 = TouristPlace(
    user_id=1,
    name="Coorg (madikeri)",
    description="it is also known as the Scotland of India",
    distance="132 km from Mangalore",
    language="Kannada",
    state=state2)
session.add(tourist_place2)
session.commit()


tourist_place3 = TouristPlace(
    user_id=1,
    name="Hampi",
    description="is an ancient village situated on"
                "the banks of Tungabhadra River ",
    distance="64 km from Bellary",
    language="Kannada",
    state=state2)
session.add(tourist_place3)
session.commit()


tourist_place4 = TouristPlace(
    user_id=1,
    name="Mysore",
    description="It is the erstwhile capital of the Mysore Maharajas,"
                "who ruled the Mysore State between 1399 & 1947",
    distance="139 km from Bangalore",
    language="Kannada",
    state=state2)
session.add(tourist_place4)
session.commit()


# create a State Tamil nadu
state3 = State(user_id=1, name="Tamil Nadu")
session.add(state3)
session.commit()


# create tourist palces in Tamil Nadu
tourist_place1 = TouristPlace(
    user_id=1,
    name="Hogenakkal",
    description="Hogenakkal Falls is a waterfall in on the"
                "Cauvery River located in Dharmapuri distric",
    distance="146 km from Bangalore",
    language="Tamil",
    state=state3)
session.add(tourist_place1)
session.commit()


tourist_place2 = TouristPlace(
    user_id=1,
    name="Kanchipuram",
    description="Kanchi is one of the most"
                "famous pilgrimage sites in Tamil Nadu",
    distance="75 km from Chennai",
    language="Tamil",
    state=state3)
session.add(tourist_place2)
session.commit()


tourist_place3 = TouristPlace(
    user_id=1,
    name="Kodaikanal",
    description="is a beautiful hill station in"
                "Dindigul district of Tamilnadu",
    distance="169 km from Coimbatore",
    language="Tamil",
    state=state3)
session.add(tourist_place3)
session.commit()


tourist_place4 = TouristPlace(
    user_id=1,
    name="Ooty",
    description="Ooty is one of the best hill stations in India",
    distance="89 km from Coimbatore",
    language="Tamil",
    state=state3)
session.add(tourist_place4)
session.commit()


print "added menu items!"
