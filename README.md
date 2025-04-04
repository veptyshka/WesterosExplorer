# Westeros Explorer

**Note:** This is my project I made for school. It is *non-commercial* made for educational and entertainment purpose.

## About Project
*Westeros Explorer* is a web-based interactive map about the world of "Game of Thrones". It allows users to explore and join various houses, learh more about their castles and history. The project is built using *Flask* for backend and *Leaflet.js* for interactive map.

## Features
- **🔐 User authentication:** Securely register and log in with hashed passwords.
- **🗺 Interactive map:** Navigate through the world of Westeros with clickable locations.
- **🏰 Select your house:** Users can choose loyalty to a noble house.
- **📚 Detailed house pages:** Learn about different houses, their castles and history.
- **🛡 Admin panel:** Three-eyed Raven keeps order in Westeros.

## How to use?
**1.** Clone the repository:
```
git clone https://github.com/your-username/westeros-explorer.git
 cd westeros-explorer
```
**2.** Install dependencies:
```
pip install -r requirements.txt
```
**3.** Initialize the database:
```
flask db upgrade
```
**4.** Run the Flask application:
```
flask run
```
and open `http://127.0.0.1:5000/` (local server) in your browser.

**5.** Enjoy!

**6.** To login as administrator, check ```utils.py``` for email and password and enter them in the login page.

## Libraries used:

### Flask (Backend)
[*Flask*](https://flask.palletsprojects.com/en/stable/)
Lightweight Python web framework.

[**Flask SQLAlchemy**](https://flask-sqlalchemy.readthedocs.io/en/stable/) - ORM for database handling.

[**Flask Bcrypt**](https://flask-bcrypt.readthedocs.io/en/1.0.1/) - secure password hashing.

[**Flask WTF**](https://flask-wtf.readthedocs.io/en/1.2.x/) - Form handling and CSRF protection.

### Leaflet.js (Frontend and Mapping)
[*Leaflet.js*](https://leafletjs.com/reference.html)
Interactive map rendering library made on JavaScript.

### Others

[**Functools**](https://docs.python.org/3/library/functools.html) - Higher-order functions and decorators.

[**Werkzeug Utilities**](https://werkzeug.palletsprojects.com/en/stable/utils/) - Utility functions for request handling.

[**WTForms**](https://wtforms.readthedocs.io/en/3.2.x/) - Utility functions for request handling.

[**Enum**](https://docs.python.org/3/library/enum.html) - Handling enumerated constants.
