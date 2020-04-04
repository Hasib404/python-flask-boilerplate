import os

from werkzeug.utils import secure_filename
from flask import (
    Flask,
    jsonify,
    send_from_directory,
    request,
    redirect,
    url_for
)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("project.config.Config")
db = SQLAlchemy(app)


class User(db.Model):
    
         
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    age = db.Column(db.String(255))
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __repr__(self):
        return '%s/%s/%s' % (self.id, self.name, self.age)


class Book(db.Model):
    
         
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    price = db.Column(db.String(255))
    
    def __init__(self, name, age):
        self.name = name
        self.author = author
        self.price = price
    
    def __repr__(self):
        return '%s/%s/%s/%s' % (self.id, self.name, self.author, self.price)
    
    

@app.route("/")
def hello_world():
    return jsonify(hello="world. How you doing?")



@app.route("/static/<path:filename>")
def staticfiles(filename):
    return send_from_directory(app.config["STATIC_FOLDER"], filename)


@app.route("/media/<path:filename>")
def mediafiles(filename):
    return send_from_directory(app.config["MEDIA_FOLDER"], filename)


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["MEDIA_FOLDER"], filename))
    return f"""
    <!doctype html>
    <title>upload new File</title>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file><input type=submit value=Upload>
    </form>
    """
    
    
    
    
@app.route('/data', methods=['POST', 'GET'])
def data():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        name = body['name']
        age = body['age']

        data = User(name, age)
        db.session.add(data)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'name': name,
            'age': age
        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        # data = User.query.all()
        data = User.query.order_by(User.id).all()
        print(data)
        dataJson = []
        for i in range(len(data)):
            # print(str(data[i]).split('/'))
            dataDict = {
                'id': str(data[i]).split('/')[0],
                'name': str(data[i]).split('/')[1],
                'age': str(data[i]).split('/')[2]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)

@app.route('/data/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = User.query.get(id)
        print(data)
        dataDict = {
            'id': str(data).split('/')[0],
            'name': str(data).split('/')[1],
            'age': str(data).split('/')[2]
        }
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = User.query.filter_by(id=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        newName = body['name']
        newAge = body['age']
        editData = User.query.filter_by(id=id).first()
        editData.name = newName
        editData.age = newAge
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is updated from PostgreSQL!'})




@app.route('/books', methods=['POST', 'GET'])
def book():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        name = body['name']
        author = body['author']
        price = body['price']
        

        book = Book(name, author, price)
        db.session.add(book)
        db.session.commit()

        return jsonify({
            'status': 'Data is posted to PostgreSQL!',
            'name': name,
            'author': author,
            'price': price
        })
    
    # GET all data from database & sort by id
    if request.method == 'GET':
        # data = Book.query.all()
        book = Book.query.order_by(Book.id).all()
        print(book)
        dataJson = []
        for i in range(len(book)):
            # print(str(data[i]).split('/'))
            dataDict = {
                'id': str(book[i]).split('/')[0],
                'name': str(book[i]).split('/')[1],
                'author': str(book[i]).split('/')[2],
                'price': str(book[i]).split('/')[3]
            }
            dataJson.append(dataDict)
        return jsonify(dataJson)

@app.route('/books/<string:id>', methods=['GET', 'DELETE', 'PUT'])
def onebook(id):

    # GET a specific data by id
    if request.method == 'GET':
        book = Book.query.get(id)
        print(book)
        dataDict = {
            'id': str(book).split('/')[0],
            'author': str(book[i]).split('/')[2],
            'price': str(book[i]).split('/')[3]
        }
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        delData = Book.query.filter_by(id=id).first()
        db.session.delete(delData)
        db.session.commit()
        return jsonify({'status': 'Data '+id+' is deleted from PostgreSQL!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        newName = body['name']
        newAuthor = body['author']
        nerwPrice = body['price']
        editData = Book.query.filter_by(id=id).first()
        editData.name = newName
        editData.author = newAuthor
        editData.price = nerwPrice
        db.session.commit()
        return jsonify({'status': 'book '+id+' is updated from PostgreSQL!'})