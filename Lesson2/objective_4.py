'''
Objective 4:  Edit Request

NOTE:  Just for fun, I added logic to issue 400 (Bad Request) when the name field is left blank

'''

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

PORT = 8080

# Create session and connect to DB
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:  
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
    
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
    
                # Objective 3:  The first message on the page should show link to create a new restaurant
                message = "<a href = '/restaurants/new'>Make a New Restaurant Here</a><br></br>"
                message += "<html><body>"
                
                for restaurant in restaurants:
                    message += restaurant.name
                    message += f"<br><a href='/restaurants/{restaurant.id}/edit'>Edit</a></br>"  # pass the restaurant.id in the edit href
                    message += "<a href=''>Delete</a>"         # pass the restaurant.id in the delete href 
                    message += "<br></br>"
                
                message += "</body></html>"
                
                self.wfile.write(message.encode())
                return

            # Objective 3:  create a "/restaurants/new" page                 
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = "<html><body>"

                # we define the "POST new restaurant name request form" block in the do_GET method 
                message += "<h1>Make a New Restaurant</h1>"
                message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>>"
                message += "<input name=newRestaurantName type='text' placeholder='New Restaurant Name'>" 
                message += "<input type='submit' value='Create'> </form>"

                # close out the HTML message body accordingly
                message += "</body></html>"

                self.wfile.write(message.encode())
                return

            # Objective 4:  create a "/restaurants/<restaurant.id>/edit" page     
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = "<html><body>"

                num = self.path.split('/')[2]
                resto = session.query(Restaurant).filter_by(id=int(num)).one()
                

                # we define the "Update restaurant name request form" block in do_GET method as well
                message += f"<h1>{resto.name}</h1>"  # display restaurant name
                message += f"<form method='POST' enctype='multipart/form-data' action='/restaurants/{num}/edit'>>"
                message += f"<input name=updateRestName type='text' placeholder={resto.name}>" 
                message += "<input type='submit' value='Rename'> </form>"
                
                # close out the HTML message body
                message += "</body></html>"

                self.wfile.write(message.encode())
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path.endswith('/restaurants/new'):  

            try:
                # this is our POST implementation logic 
                # the cgi.parse_header would parse the header into the main value (ctype) and the parameter dictionary (pdict):
                # - 'ctype' = the encode type  
                # - 'pdict' = parameter dictionary that containts the parameters in the "Content-Type" header
                # cgi.parse processes user input  submitted through the HTML form defined in the do_GET function 
                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    pdict['CONTENT-LENGTH'] = self.headers.get('content-length')
                    # get all the key/field values of the multipart/form-data from the pdict 
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    # here we retrieve the new restaurant name value that was entered in the 'POST' form 
                    # convert the name value to he machine-readable unicode binary format (decode utf-8)
                    # NOTE: fields.get() returns a LIST with the value as the first element in the list  so we need to do fields.get()[0]
                    messagecontent = fields.get('newRestaurantName')[0].decode('utf-8')
                
                    #  sqlalchemy create new restaurant object
                    newRestaurant = Restaurant(name=messagecontent)
                    session.add(newRestaurant)
                    session.commit() 

                    # execute the following after session.commit() success 
                    self.send_response(301)  # HTTP POST() redirect request
                    self.send_header('Content-type', 'text/html')
                    # once we submit our form we want our server to redirect to the `/restaurants` main page  
                    # for send_header to redirect link we specify 'Location' for the first arg and the path for second arg
                    self.send_header('Location', '/restaurants')
                    # always do end_headers AFTER ALL headers are sent
                    self.end_headers()

            except:
                pass

        if self.path.endswith('/edit'):  

            try:

                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    pdict['CONTENT-LENGTH'] = self.headers.get('content-length')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    
                    # convert messagecontent from binary to string so we can run sql query
                    messagecontent = fields.get('updateRestName')[0].decode('utf-8')

                    # get restaurant ID from the server path
                    num = int(self.path.split('/')[2])

                    if not messagecontent:
                        self.send_error(400, 'Restaurant Name field cannot be empty')
                    else:
                        # update restaurant object
                        # resto = Restaurant(id=num.decode('utf-8')).one()    # decode id value to binary
                        resto = session.query(Restaurant).filter_by(id=num).one()
                        resto.name = messagecontent 
                        session.add(resto)
                        session.commit() 

                    # execute the following after session.commit() success 
                    self.send_response(301)  # HTTP POST() successful response
                    self.send_header('Content-type', 'text/html')
                    # the following code redirects to the `/restaurants` page, which 
                    # runs a listing of restaurants that includes the updated restaurant name
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            except:
                pass

def main():
    try:
        server = HTTPServer(('', PORT), webServerHandler)
        print('Web server running...open localhost:8080/restaurants in your browser')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()
