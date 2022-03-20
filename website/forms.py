from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length

class PacienteForm(FlaskForm):
    nome = StringField(validators=[DataRequired(), Length(min=3)])
    data_atendimento = DateField(validators=[DataRequired()])
    procedimento = SelectField(coerce=int)
    plano_saude = SelectField(coerce=int)
    submit = SubmitField('Cadastrar Paciente')


#------------------------------------------------------
# CRIAR FORM PARA ADICIONAR PLANO

class PlanoForm(FlaskForm):
    descr = StringField(validators=[DataRequired(), Length(min=2)])
    submitplano = SubmitField('Incluir')

#------------------------------------------------------
# CRIAR FORM PARA ADICIONAR PROCEDIMENTO

class ProcedimentoForm(FlaskForm):
    descr = StringField(validators=[DataRequired(), Length(min=2)])
    submitprocedimento = SubmitField('Incluir')

class FiltroForm(FlaskForm):
    plano_saude = SelectField('Plano de Saúde',coerce=int)
    faturamento = SelectField('Faturamento',choices=['Faturado', 'Não Faturado'])
    data_de = DateField('Data de')
    data_ate = DateField('Data até')
    submit = SubmitField('Filtrar')
