# DecisionTreeApp
I built this application to help with decision paralysis and cyclical thinking. It recursively walks a user through the best, realistic, and worse cases of going through with a decision. 
The process proves it to the user that they thought through the most important avenues of committing to a decision and hopefully leads to action or putting ideas to rest. At the end, the user
is shown a tree of their outcomes and can download a png of it. 
  
Link to the project: https://decisiontreeapp.onrender.com/

# Tech Stack
Front end: HTML/CSS/JavaScript  
Back end: Python (Flask), Jinja2  
Database: SQLite (via SQLAlchemy)  
Deployment: Render

# Techincal Details
The data is stored as tree nodes in a SQLite database, defined in "tree.py". The data is displayed by traversing the nodes recursively. The two JavaScript files ("png.js" and "duplicate.js") are used to download a png of the tree and 
handle a duplicate outcome button respectively. The client data is tracked in seperate sessions using unique tree_ids. 

# Lessons Learned
This was my first finished full stack application. Through this project, I:  
- Learned the basics of Flask(app routing, Jinja2) and improved my skills of HTML/CSS/JavaScript.
- Gained an understanding of frontend-backend communication
- Figured out how to store data into SQLite and session tracking

