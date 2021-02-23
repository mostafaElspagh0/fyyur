Fyyur
-----

this is my submissiion for assignment in udacity full stack nano degree

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.


## Tech Stack (Dependencies)
  **python3**
  **flask**
  **SQLAlchemy**
  **postgresql**
  **Flask-Migrate**

## Main Files: Project Structure

  ```sh
     fyyur/
      ├──  .gitignore
      ├──  app.py
      ├──  config.py
      ├──  database_uri.py
      ├──  erd.dia
      ├──  error.log
      ├──  fabfile.py
      ├──  README.md
      ├──  requirements.txt
      ├──  controllers/
      ├──  enums/
      ├──  forms/
      │      └── validators/
      ├──  migrations/
      ├──  models/
      ├──  static
      │      ├── css 
      │      ├── font
      │      ├── ico
      │      ├── img
      │      └── js
      └── templates
            ├── errors
            ├── forms
            ├── layouts
            └── pages
  ```

## Setup

1. **Install the dependencies:**
```
pip install -r requirements.txt
```


2. **config database uri server:**
  
  *  install any database that is supported by sqlalchemy that includes (SQLite, Postgresql, MySQL, Oracle, MS-SQL, Firebird, Sybase)
  *  configure the database uri in database_uri.py


3. **Run the development server:**
```
export FLASK_APP=myapp
export FLASK_ENV=development # enables debug mode
python3 app.py
```


4. **Verify on the Browser**<br>
Navigate to project homepage [http://127.0.0.1:5000/](http://127.0.0.1:5000/) or [http://localhost:5000](http://localhost:5000) 

