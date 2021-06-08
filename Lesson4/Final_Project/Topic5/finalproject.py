from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

# Prepare database for use
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants/')
def listrestaurants():
    return 'This page returns the list of restaurants'

@app.route('/restaurants/new')
def newRestaurant():
    return 'This page will show the Create New Restaurant template'

@app.route('/restaurants/<int:restaurant_id>/edit')
def updateRestaurant(restaurant_id):
    return f'This page will show the Edit Restaurant template for restaurant id {restaurant_id}'

@app.route('/restaurants/<int:restaurant_id>/delete')
def delRestaurant(restaurant_id):
    return f'This page will show the Delete Restaurant template for restaurant id {restaurant_id}'

@app.route('/restaurants/<int:restaurant_id>/menus')
def listRestMenu(restaurant_id):
    return f'This page returns the list of menus for Restaurant id {restaurant_id}'

@app.route('/restaurants/<int:restaurant_id>/menus/new')
def NewRestMenu(restaurant_id):
    return f'This page displays Create Menu page for Restaurant id {restaurant_id}'

@app.route('/restaurants/<int:restaurant_id>/menus/<int:menu_id>/edit')
def editRestMenu(restaurant_id, menu_id):
    return f"This page displays Edit Menu page for Restaurant id {restaurant_id}'s menu #{menu_id}"

@app.route('/restaurants/<int:restaurant_id>/menus/<int:menu_id>/delete')
def delRestMenu(restaurant_id, menu_id):
    return f"This page displays Delete Menu page for Restaurant id {restaurant_id}'s menu #{menu_id}"

if __name__ == '__main__':

    # debug mode ON
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded=False)