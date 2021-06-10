from flask import Flask, request, render_template, url_for, jsonify, flash
# from flask.templating import render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from werkzeug.utils import redirect
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

# Prepare database for use
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# convert price to a float with two decimal numbers
def convert(price):
    if not price:
        price = '0'  # need price to be text value

    if '.' not in price: # whole number only
        return f"{int(float(price)):.2f}"
    else:
        return price

@app.route('/restaurants/JSON')
def restaurantJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurant=[i.serialize for i in restaurants])

@app.route('/restaurants/<int:restaurant_id>/menus/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItems=[i.serialize_menu for i in menuItems])

@app.route('/restaurants/<int:restaurant_id>/menus/<int:menu_id>/JSON')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menuItem = session.query(MenuItem).filter_by(restaurant_id=restaurant.id, id=menu_id).one()
    return jsonify(MenuItem=[menuItem.serialize_menu])

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    # return 'This page returns the list of restaurants'
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new', methods=['GET','POST'])
def newRestaurant():
    if request.method == 'POST':
        if len((request.form["name"]).replace(' ','')) > 0:
            restaurant = Restaurant(name=request.form['name'])
            session.add(restaurant)
            session.commit()
            flash("New Restaurant Created", "success")
            return(redirect(url_for('showRestaurants')))
        else:
            flash("New Restaurant Name cannot be Blank ", "error") 
            return(redirect(url_for('newRestaurant')))
    else:
        # return 'This page will show the Create New Restaurant template'
        return render_template('newRestaurant.html')

@app.route("/restaurants/<int:restaurant_id>/edit", methods=['GET','POST'])
def editRestaurant(restaurant_id):
    # return f'This page will show the Edit Restaurant template for restaurant id {restaurant_id}'
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    orig_name = restaurant.name
    if request.method == 'POST':
        if len((request.form["rname"]).replace(' ','')) > 0 or request.form["rname"] == orig_name:
            restaurant.name = request.form['rname']
            session.add(restaurant)
            session.commit()
            flash("Restaurant Successfully Edited", "success")
            return redirect(url_for('showRestaurants'))
        else:
            flash("Restaurant Name Unchanged or left blank", "error")
            return redirect(url_for('editRestaurant', restaurant_id = restaurant_id))
    else:
        return render_template('EditRestaurant.html', restaurant =restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()            
        flash("Restaurant Successfully Deleted", "success")
        return redirect(url_for('showRestaurants'))
    else:
    # return f'This page will show the Delete Restaurant template for restaurant id {restaurant_id}'
        return render_template('DeleteRestaurant.html', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/menus')
def showMenus(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    restaurant_name = restaurant.name
    restaurant_id = restaurant.id
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menus.html', items=items, restaurant_name = restaurant_name, restaurant_id = restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menus/new', methods=['GET','POST'])
def newMenu(restaurant_id):
    if request.method == 'POST':
        #  NOTE: New menu will NOT BE CREATED if menu name is left blank.  Also, menu price and
        #  menu description will be set to default values if not provided.  The menu course
        # is defaulted to 'Entree' under the NewMenuItem.html template
        if len((request.form["menuName"]).replace(' ','')) > 0:
            cost = convert(request.form['price'])
            menu = MenuItem(name=request.form['menuName'], price=cost,
                            description=request.form['description'] or 'No info available',
                            course=request.form['course'], restaurant_id = restaurant_id)
            session.add(menu)
            session.commit()
            flash("New Menu Item Created", "success")
            return redirect(url_for('showMenus',restaurant_id=restaurant_id))
        else:
            flash("New Menu Item Name cannot be Blank!", "error")
            return redirect(url_for('newMenu',restaurant_id=restaurant_id))
    else:
        return render_template('NewMenuItem.html',restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menus/<int:menu_id>/edit', methods=['GET','POST'])
def editMenu(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id).one()
    orig_item = item
    if request.method == 'POST':
        post_updates = 0
        # ONLY do updates if AT LEAST one field is updated (avoid unncessary database updates)
        if len((request.form["menuName"]).replace(' ','')) > 0 and request.form["menuName"] != orig_item.name:
            item.name = request.form["menuName"]
            post_updates += 1
        
        # convert request.form['price'] to a float with 2 decimal places as needed
        cost = convert(request.form['price'])
        if cost != orig_item.price:
            item.price = cost
            post_updates += 1
        if request.form["description"] and request.form["description"] != orig_item.description:
            item.description = request.form["description"] or 'no info available'
            post_updates += 1
        if request.form["course"] != orig_item.course:
            item.course = request.form["course"]
            post_updates += 1

        if post_updates:
            session.add(item)
            session.commit()
            flash("Menu Item Successfully Edited", "success")
            return redirect(url_for('showMenus', restaurant_id=restaurant_id))           
        else:
            flash("WARNING: No changes made or name left blank for this menu item", "error")
            return redirect(url_for('editMenu', restaurant_id=restaurant_id, menu_id = menu_id))
    else:
        return render_template('EditMenuItem.html', item=item, menu_id = item.id, restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menus/<int:menu_id>/delete', methods=['GET','POST'])
def deleteMenu(restaurant_id, menu_id):
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method== 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Menu Item Successfully Deleted", "success")
   
        return redirect(url_for('showMenus', restaurant_id=restaurant_id))
    else:
    # return f"This page displays Delete Menu page for Restaurant id {restaurant_id}'s menu #{menu_id}"
        return render_template('DeleteMenuItem.html', restaurant_id= restaurant_id, item=itemToDelete)

if __name__ == '__main__':

    # debug mode ON
    app.debug = True
    app.secret_key = 'super_secret_key'
    app.run(host='0.0.0.0', port=5000,threaded=False)