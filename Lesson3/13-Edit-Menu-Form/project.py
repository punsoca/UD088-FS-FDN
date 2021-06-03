'''
This version of project.py that covers Lesson3 Topics #9 - #11:
- use render_template(<template.html>, <parameters to pass to the html>
'''

from flask import Flask, render_template, redirect, request, url_for

app = Flask(__name__)

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# List Restaurants
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    try:

        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

        return render_template('menu.html', restaurant=restaurant, items=items)

    except:
        pass


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        #  the POST method we will get the input info from the "POST form" from the 
        #  template (i.e., login.html) using request.form["<input name>"], in this case, menuName
        # 
        # note the following line only provides the menu name, but not its price or description
        #
        newItem = MenuItem(
            name=request.form['menuName'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()

        # redirect to 'restaurantMenu' page where it should display the restaurant menus including
        # the latest addition
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # the GET method will just render the newmenuitem template
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

# Lesson 3 Topic 13 Edit Menu Item Form Quiz (also includes editmenuitem.html)

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            session.add(editedItem)
            session.commit()
            return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
         # this is the GET method section, it will just render the editmenuitemhtml template
         #
         # USE THE render_template FUNCTION BELOW TO SEE THE VARIABLES YOU
         # SHOULD USE IN YOUR editmenuitem TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, item=editedItem)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a new menu item. Task 3 complete!"



if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
