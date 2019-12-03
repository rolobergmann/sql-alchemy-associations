from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
#Join Tables
contract_table = db.Table('contract', db.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("project_id", db.Integer, db.ForeignKey("project.id"))
)

# User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(256), unique=False, nullable=False)
    last_name = db.Column(db.String(256), unique=False, nullable=False)
    bank_account = db.relationship("BankAccount", uselist=False, back_populates="user")
    projects = db.relationship("Project", secondary=contract_table, back_populates="users")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "username": self.username,
            "email": self.email
        }

# One to One
class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="bank_account")

# One to Many
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __repr__(self):
        return '<Pet %r>' % self.name
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

# Many to Many

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=False, nullable=False)
    code = db.Column(db.String(256), unique=True, nullable=False)
    users = db.relationship("User", secondary=contract_table, back_populates="projects")

    def __repr__(self):
        return '<Project %r>' % self.name

    def serialize(self):
        return {
            "name": self.name,
            "code": self.code
        }
