from flask import Flask
from flask.templating import render_template
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

# #-Prepare database for use
# engine = create_engine('sqlite:///restaurantmenu.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurant_id = int(restaurant['id'])

restaurants = [
    {'name': 'The CRUDdy Crab', 'id': '1'}, 
    {'name':'Blue Burgers', 'id':'2'},
    {'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ 
    {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, 
    {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},
    {'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},
    {'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},
    {'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]

item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
menu_id = 1



@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    # return 'This page returns the list of restaurants'
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new')
def newRestaurant():
    # return 'This page will show the Create New Restaurant template'
    return render_template('newRestaurant.html')

@app.route("/restaurants/<int:restaurant_id>/edit")
def editRestaurant(restaurant_id):
    # return f'This page will show the Edit Restaurant template for restaurant id {restaurant_id}'
    return render_template('editRestaurant.html', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    # return f'This page will show the Delete Restaurant template for restaurant id {restaurant_id}'
    return render_template('deleteRestaurant.html', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/menus')
def showMenus(restaurant_id):
    # return f'This page returns the list of menus for Restaurant id {restaurant_id}'
    return render_template('menus.html', items=items)


@app.route('/restaurants/<int:restaurant_id>/menus/new')
def newMenu(restaurant_id):
    # return f'This page displays Create Menu page for Restaurant id {restaurant_id}'
    return render_template('NewMenuItem.html')

@app.route('/restaurants/<int:restaurant_id>/menus/<int:menu_id>/edit')
def editMenu(restaurant_id, menu_id):
    # return f"This page displays Edit Menu page for Restaurant id {restaurant_id}'s menu #{menu_id}"
    return render_template('EditMenuItem.html', item=item)

@app.route('/restaurants/<int:restaurant_id>/menus/<int:menu_id>/delete')
def deleteMenu(restaurant_id, menu_id):
    # return f"This page displays Delete Menu page for Restaurant id {restaurant_id}'s menu #{menu_id}"
    return render_template('DeleteMenuItem.html', item=item)

if __name__ == '__main__':

    # debug mode ON
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded=False)