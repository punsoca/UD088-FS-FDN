'''
opening http://localhost:8080/restaurants lists all the restaurants in the database
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
                message = ""
                message += "<html><body>"
                
                for restaurant in restaurants:
                    message += restaurant.name
                    message += "</br>"
                
                message += "</body></html>"
                
                self.wfile.write(message.encode())
                return
            
            else:
                self.send_error(404, f"File Not Found localhost:{PORT}{self.path}")
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


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


# '''
# opening http://localhost:8080/restaurants lists all the restaurants named in the database
# '''
# # from http.server import BaseHTTPRequestHandler, HTTPServer
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from .database_setup import Base, Restaurant


# engine = create_engine('sqlite:///restaurantMenu.db')
# Base.metadata.bind = engine
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

# restaurants = session.query(Restaurant).all()
# for restaurant in restaurants:
#     print(restaurant.name)

# class WebServerHandler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         if self.path.endswith("/hello"):
#             # English language response
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             message = ""
#             message += "<html><body>"
#             message += "<h1>Hello!</h1>"
#             message += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
#             message += "</body></html>"

#             self.wfile.write(message.encode())
#             print(message)
#             return




# def main():
#     try:
#         port = 8080
#         server = HTTPServer(('', port), WebServerHandler)
#         print(f"Web Server running on port {port}")
#     except:
#         pass


# if __name__ == '__main__':
#     main()