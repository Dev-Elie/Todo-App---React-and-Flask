from flask import Flask,jsonify,request,json

from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text,nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.content

def todo_serializer(todo):
    return {
    'id':todo.id,
    'content':todo.content
    }


@app.route('/api',methods = ['GET'])
def index():
    # the iterable
    todo = Todo.query.all()
    # map takes in a function and an iterable
    return jsonify([*map(todo_serializer,todo)])


@app.route('/api/create',methods = ['POST'])
def create():
    request_data = json.loads(request.data) 
    todo = Todo(content = request_data['content'])
    db.session.add(todo)
    db.session.commit()

    return {'201':'Todo created sucessfully'}

@app.route('/api/<int:id>')
def show(id):
    todo = Todo.query.filter_by(id=id)
    return jsonify([*map(todo_serializer,todo)])


@app.route('/api/<int:id>',methods=['POST'])
def delete(id):
    request_data = json.loads(request.data)
    Todo.query.filter_by(id=request_data['id']).delete()
    db.session.commit()

    return {'204':'Deleted sucessfully'}



if __name__ == "__main__":
    app.run(debug=True) 