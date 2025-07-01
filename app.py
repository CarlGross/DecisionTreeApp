from flask import Flask, render_template, request, redirect, session
from tree import db, Node
import secrets

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secrets.token_hex(16)
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        root = Node(scenario=request.form['root'])
        root.level = 0
        db.session.add(root)
        db.session.commit()
        session['queue'] = [root.id]
        return redirect(f'/questions/')
    else:
        return render_template('index.html')

@app.route('/questions/', methods=['POST', 'GET'])
def questions():
    queue = session.get('queue', [])
    node_id = queue[0]
    currNode = Node.query.get_or_404(node_id)
    if request.method == 'POST':
        level = currNode.level + 1
        best = Node(scenario=request.form['best_case'], level=level)
        realistic = Node(scenario=request.form['realistic_case'], level=level)
        worst = Node(scenario=request.form['worst_case'], level=level)
        db.session.add_all([best, realistic, worst])
        currNode.best = best
        currNode.realistic = realistic
        currNode.worst = worst
        best.parent_id = node_id
        realistic.parent_id = node_id
        db.session.commit()

        worst.parent_id = node_id
        queue += [best.id, realistic.id, worst.id]
        queue.pop(0)
        session['queue'] = queue
        
        return redirect('/questions/')
    return render_template('questions.html', currNode=currNode, level=currNode.level + 1)

@app.route('/display/', methods=['POST', 'GET'])
def display():
    return render_template('display.html', nodes=Node.query.all())

if __name__ == '__main__':
   
    app.run(debug=True)