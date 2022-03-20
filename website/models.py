from email.policy import default
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Plano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(20))

class Procedimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descr = db.Column(db.String(20))

class Consulta(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), primary_key=True)
    plano_id = db.Column(db.Integer, db.ForeignKey('plano.id'), primary_key=True)
    procedimento_id = db.Column(db.Integer, db.ForeignKey('procedimento.id'), primary_key=True)
    data_atendimento = db.Column(db.Date, primary_key=True)
    faturamento = db.Column(db.Date)
    valor = db.Column(db.Numeric(precision=20,scale=2))
    pagamento = db.Column(db.Boolean, default=False)


    user = db.relationship('User')
    paciente = db.relationship('Paciente')
    plano = db.relationship('Plano')
    procedimento = db.relationship('Procedimento')

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    data_cadastro = db.Column(db.Date, default=func.now())
    consulta = db.relationship('Consulta')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def as_dict(self):
        return {'nome': self.nome}

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    paciente = db.relationship('Paciente')
    consulta = db.relationship('Consulta')
