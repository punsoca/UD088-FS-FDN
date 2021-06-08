from flask import Flask, request, render_template, url_for
# from flask.templating import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import redirect
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

#-Prepare database for use
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
# restaurant_id = int(restaurant['id'])

# restaurants = [
#     {'name': 'The CRUDdy Crab', 'id': '1'}, 
#     {'name':'Blue Burgers', 'id':'2'},
#     {'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
# items = [ 
#     {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, 
#     {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},
#     {'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},
#     {'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},
#     {'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]

item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}
# menu_id = 1

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    # return 'This page returns the list of restaurants'
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        if request.form['menuName']:
            restaurant = Restaurant(name=request.form['name'])
            session.add(restaurant)
            session.commit()
        return(redirect(url_for('showRestaurants')))
    else:
        # return 'This page will show the Create New Restaurant template'
        return render_template('newRestaurant.html')

@app.route("/restaurants/<int:restaurant_id>/edit", methods=['GET','POST'])
def editRestaurant(restaurant_id):
    # return f'This page will show the Edit Restaurant template for restaurant id {restaurant_id}'
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['rname']:
            restaurant.name = request.form['rname']
            session.add(restaurant)
            session.commit()

        return redirect(url_for('showRestaurants'))
    else:
        return render_template('EditRestaurant.html', restaurant =restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
    # return f'This page will show the Delete Restaurant template for restaurant id {restaurant_id}'
        return render_template('DeleteRestaurant.html', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/menus')
def showMenus(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    # return f'This page returns the list of menus for Restaurant id {restaurant_id}'
    return render_template('menus.html', items=items, restaurant = restaurant)

@app.route('/restaurants/<int:restaurant_id>/menus/new', methods=['GET','POST'])
def newMenu(restaurant_id):
    # return f'This page displays Create Menu page for Restaurant id {restaurant_id}'
    if request.method == 'POST':
        if request.form['menuName']:
            menu = MenuItem(name=request.form['menuName'], price=request.form['price'],
                            description=request.form['description'], course=request.form['course'],
                            restaurant_id = restaurant_id)
            session.add(menu)
            session.commit()

        return redirect(url_for('showMenus',restaurant_id=restaurant_id))
    else:
        return render_template('NewMenuItem.html',restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menus/<int:menu_id>/edit', methods=['GET','POST'])
def editMenu(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id).one()
    if request.method == 'POST':
        if request.form["menuName"]:
            item.name = request.form["menuName"]
        if request.form["price"]:
            item.price = request.form["price"]
        if request.form["description"]:
            item.description = request.form["description"]
        if request.form["course"]:
            item.course = request.form["course"]
        session.add(item)
        session.commit()

        return redirect(url_for('showMenus', restaurant_id=restaurant_id))
    else:
        return render_template('EditMenuItem.html', item=item, menu_id = item.id, restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menus/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenu(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method== 'POST':
        session.delete(itemToDelete)
        session.commit()
    
        return redirect(url_for('showMenus', restaurant_id=restaurant_id))
    else:
    # return f"This page displays Delete Menu page for Restaurant id {restaurant_id}'s menu #{menu_id}"
        return render_template('DeleteMenuItem.html', restaurant_id= restaurant_id, item=itemToDelete)

if __name__ == '__main__':

    # debug mode ON
    app.debug = True
    app.run(host='0.0.0.0', port=5000,threaded=False)