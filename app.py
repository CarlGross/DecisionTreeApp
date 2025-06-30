from flask import Flask, render_template
from tree import db, Node

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
# with app.app_context():
#     db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
   
    app.run(debug=True)