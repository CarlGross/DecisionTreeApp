from flask import Flask, render_template, request, redirect, session
from tree import db, Node
import secrets
import uuid

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = secrets.token_hex(16)
db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()

def get_duplicate(scenario, tree_id):
    return db.session.query(Node).filter(Node.tree_id == tree_id).filter(Node.scenario == scenario).first()

def duplicate_increment(curr):
    curr.off_realistic -= 1
    if curr.best:
        duplicate_increment(curr.best)
    if curr.realistic:
        duplicate_increment(curr.realistic)
    if curr.worst:
        duplicate_increment(curr.worst)



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        tree_id = str(uuid.uuid4())
        session['tree_id'] = tree_id
        root = Node(scenario=request.form['root'], level=0, off_realistic=0, tree_id=tree_id)
        db.session.add(root)
        db.session.commit()
        session['queue'] = [root.id]
        return redirect('/questions/')
    else:
        return render_template('index.html')

@app.route('/questions/', methods=['POST', 'GET'])
def questions():
    tree_id = session.get('tree_id')
    queue = session.get('queue', [])
    if queue == []:
        return redirect('/tree/')
    node_id = queue[0]
    currNode = Node.query.get_or_404(node_id)
    if currNode.level == 3:
        return redirect('/tree/')
    if request.method == 'POST':
        level = currNode.level + 1
        best_input = request.form['best_case']
        realistic_input = request.form['realistic_case']
        worst_input = request.form['worst_case']

        best_exist = get_duplicate(best_input, tree_id)
        realistic_exist = get_duplicate(realistic_input, tree_id)
        worst_exist = get_duplicate(worst_input, tree_id)

        best = Node(scenario=best_input, level=level, tree_id=tree_id, off_realistic=currNode.off_realistic + 1)
        realistic = Node(scenario=realistic_input, level=level, tree_id=tree_id, off_realistic=currNode.off_realistic)
        worst = Node(scenario=worst_input, level=level, tree_id=tree_id, off_realistic=currNode.off_realistic + 1)
        if best_input == realistic_input:
            db.session.add(realistic)
            currNode.realistic = realistic
            realistic.parent_id = node_id
            if realistic_exist:
                duplicate_increment(realistic_exist)
            db.session.commit()
        else:
            db.session.add_all([best, realistic])
            currNode.realistic = realistic
            currNode.best = best
            realistic.parent_id = node_id
            best.parent_id = node_id
            if realistic_exist:
                duplicate_increment(realistic_exist)
            if best_exist: 
                duplicate_increment(best_exist)
            db.session.commit()
            if not best_exist and best_input != '':
                queue += [best.id]
            
        
        if not realistic_exist and realistic_input != '':
            queue += [realistic.id]

        if realistic_input != worst_input:
            db.session.add(worst)
            currNode.worst = worst
            worst.parent_id = node_id
            if worst_exist:
                duplicate_increment(worst_exist)
            db.session.commit()
            if not worst_exist and worst_input != '':
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
    tree_id = session.get('tree_id')
    root = Node.query.filter_by(tree_id=tree_id, level=0).first()
    return render_template('tree.html', root=root)

if __name__ == '__main__':
   
    app.run(debug=True)