from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD Operations from Lesson 1
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
                    message += "<br><a href=''>Edit</a></br>"
                    message += "<a href=''>Delete</a>"
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
                message += "<h1>Make a New Restaurant</h1>"
                message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>>"
                message += "<input name=newRestaurantName type='text' placeholder='New Restaurant Name'>" 
                message += "<input type='submit' value='Create'> </form>"
                message += "</body></html>"

                self.wfile.write(message.encode())
                return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        if self.path.endswith('/restaurants/new'):  

            try:

                ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                    pdict['CONTENT-LENGTH'] = self.headers.get('content-length')
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')[0].decode('utf-8')
                
                    # create new restaurant object
                    newRestaurant = Restaurant(name=messagecontent)
                    session.add(newRestaurant)
                    session.commit() 

                    # execute the following after session.commit() success 
                    self.send_response(301)  # HTTP POST() successful response
                    self.send_header('Content-type', 'text/html')
                    # the following code redirects to the `/restaurants` page, which 
                    # runs a listing of restaurants that includes the new restaurant 
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            except:
                pass

def main():
    try:
        server = HTTPServer(('', 8080), webServerHandler)
        print('Web server running...open localhost:8080/restaurants in your browser')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()

if __name__ == '__main__':
    main()
