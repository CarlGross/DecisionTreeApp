from flask import Flask, render_template, request, redirect
from tree import db, Node

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        root = Node(scenario=request.form['root'])
        db.session.add(root)
        db.session.commit()
        return redirect(f'/questions/{root.id}')
    else:
        return render_template('index.html')

@app.route('/questions/<int:node_id>', methods=['POST', 'GET'])
def questions(node_id):
    currNode = Node.query.get_or_404(node_id)
    if request.method == 'POST':
        best = Node(scenario=request.form['best_case'])
        realistic = Node(scenario=request.form['realistic_case'])
        worst = Node(scenario=request.form['worst_case'])
        db.session.add_all([best, realistic, worst])
        currNode.best = best
        currNode.realistic = realistic
        currNode.worst = worst
        best.parent_id = node_id
        realistic.parent_id = node_id
        worst.parent_id = node_id
        db.session.commit()
       
        return redirect('/display/')
    return render_template('questions.html', currNode=currNode)

@app.route('/display/', methods=['POST', 'GET'])
def display():
    return render_template('display.html', nodes=Node.query.all())

if __name__ == '__main__':
   
    app.run(debug=True)