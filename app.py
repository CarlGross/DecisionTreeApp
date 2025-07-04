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
        return redirect('/questions/')
    else:
        return render_template('index.html')

@app.route('/questions/', methods=['POST', 'GET'])
def questions():
    queue = session.get('queue', [])
    node_id = queue[0]
    currNode = Node.query.get_or_404(node_id)
    if currNode.level == 3:
        return redirect('/tree/')
    if request.method == 'POST':
        level = currNode.level + 1
        best_input = request.form['best_case']
        realistic_input = request.form['realistic_case']
        worst_input = request.form['worst_case']
        best = Node(scenario=best_input, level=level)
        realistic = Node(scenario=realistic_input, level=level)
        worst = Node(scenario=worst_input, level=level)
        if best_input == realistic_input:
            db.session.add(realistic)
            realistic.parent_id = node_id
            currNode.realistic = realistic
            db.session.commit()
        else:
            db.session.add_all([best, realistic])
            currNode.realistic = realistic
            currNode.best = best
            realistic.parent_id = node_id
            best.parent_id = node_id
            db.session.commit()
            queue += [best.id]

        queue += [realistic.id]

        if realistic_input != worst_input:
            db.session.add(worst)
            currNode.worst = worst
            worst.parent_id = node_id
            db.session.commit()
            queue += [worst.id]

        queue.pop(0)
        session['queue'] = queue
        return redirect('/questions/')
    return render_template('questions.html', currNode=currNode, level=currNode.level + 1)

@app.route('/display/', methods=['POST', 'GET'])
def display():
    return render_template('display.html', nodes=Node.query.all())

@app.route('/tree/', methods=['POST', 'GET'])
def tree():
    root = Node.query.order_by(Node.id).first()
    return render_template('tree.html', root=root)

if __name__ == '__main__':
   
    app.run(debug=True)