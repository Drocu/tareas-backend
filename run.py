from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://uj3f3vlzdzgahm5t:Hvc7HPySFvXfBf8DcbXD@b0pykgnwcvrb5qpry8ah-mysql.services.clever-cloud.com:3306/b0pykgnwcvrb5qpry8ah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

### creamos clases del ORM ###
class Tarea(db.Model):
    id = db.Column(db.Integer,primary_key=True) # ID int primary key
    descripcion = db.Column(db.String(200),nullable=False) # descripcion varchar(200) NOT NULL
    estado = db.Column(db.String(100),nullable=False) # estado varchar(100) NOT NULL
    
    def __init__(self,descripcion,estado):
        self.descripcion = descripcion
        self.estado = estado
    
### esquemas ###
ma = Marshmallow(app)
class TareaSchema(ma.Schema):
    class Meta:
        fields = ('id','descripcion','estado')
            
#### convertimos la clase en una tabla : MIGRACION
db.create_all()
print("se creo la tabla en la base de datos")
    
@app.route('/')
def index():
    context = {
        'status':True,
        'content':'servicor activo'
    }
    return jsonify(context)


@app.route('/tarea',methods=['POST'])
def setTarea():
    descripcion = request.json['descripcion']
    estado = request.json['estado']
    
    nuevaTarea= Tarea(descripcion,estado)
    db.session.add(nuevaTarea)
    db.session.commit()
    
    data_schema = TareaSchema()
    
    context={
        'status':True,
        'content': data_schema.dump(nuevaTarea)
    }
    
    return jsonify(context)

@app.route('/tarea', methods=['GET'])
def getTarea():
    data = Tarea.query.all() #select * from tarea
    print(data)
    
    data_schema = TareaSchema(many=True)
       
    context = {
        'status':True,
        'content': data_schema.dump(data)
    }
    return jsonify(context)

@app.route('/tarea/<id>',methods=['PUT'])
def updateTarea(id):
    descripcion = request.json['descripcion']
    estado = request.json['estado']
    
    updateTarea = Tarea.query.get(id)
    updateTarea.descripcion = descripcion
    updateTarea.estado = estado
    db.session.commit()
    
    data_schema = TareaSchema()
    
    context = {
        'status':True,
        'content':data_schema.dump(updateTarea)
    }
    
    return jsonify(context)

@app.route('/tarea/<id>',methods=['DELETE'])
def deleteTarea(id):
    
    deleteTarea = Tarea.query.get(id)
    db.session.delete(deleteTarea)
    db.session.commit()
    
    data_schema = TareaSchema()
    
    context = {
        'status':True,
        'content':data_schema.dump(deleteTarea)
    }
    
    return jsonify(context)

app.run(debug=True)