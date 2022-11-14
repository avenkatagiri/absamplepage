from flask import Flask, request

app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:SmG%40mysql22@localhost:3306/AWSPOC'    

db=SQLAlchemy(app) 

# db = connector.connect(user="root",passwd="SmG@mysql22",host="localhost", port=3306, auth_plugin='mysql_native_password', database='AWSPOC' ) 

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)   
    firstname = db.Column(db.String(255), nullable=False)  
    lastname = db.Column(db.String(255), nullable=False)  
    email = db.Column(db.String(255), unique=True)  
    dob = db.Column(db.Date)
    
    def __repr__(self) -> str:
        return f"{self.firstname}-{self.lastname}" 

@app.route('/')
def index():
    return 'Hello!  '


@app.route('/employees')
def get_employees():
        emps = Employees.query.all()
        output = []
        
        for employee in emps:
            output.append( {'firstName' : employee.firstname, 'lastName' : employee.lastname, 'id' : employee.id })
            return output
      
@app.route('/employees/<id>')
def get_employee(id):
      emp =  Employees.query.get_or_404(id)
      return {'firstname' : emp.firstname }
  
  
@app.route('/employees', methods=['POST'])
def create_employee():
    employee = Employees(firstname = request.json['firstname'], lastname = request.json['firstname'], email =  request.json['email'], dob = request.json['dob'])
    db.session.add(employee)
    db.session.commit()
    return {'id' : employee.id}