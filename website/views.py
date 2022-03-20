from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from .forms import PlanoForm, ProcedimentoForm, PacienteForm, FiltroForm
from .models import Paciente, Plano, Procedimento, Consulta, User
from . import db
import json

views = Blueprint('views', __name__)

#--------------------------------------------------------------------

#ROUTE PARA HOME
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    plano = ""
    faturamento = ""
    data_de = ""
    data_ate = ""

    form = FiltroForm()

    list_plano_saude = db.session.query(Plano)
    form.plano_saude.choices = [(g.id, g.descr) for g in list_plano_saude]

    filtrovalor = db.session.query(Consulta)
        
    if form.validate_on_submit():

        plano = form.plano_saude.data
        faturamento_form = form.faturamento.data
        data_de = form.data_de.data
        data_ate = form.data_ate.data

        if faturamento_form == "Faturado":
            faturamento = 1
        
        else:
            faturamento = 0

        plano_id = db.session.query(Plano).filter_by(id = plano).first()

        filtrovalor = db.session.query(Consulta).filter(    Consulta.user_id == current_user.id,
                                                            Consulta.pagamento == faturamento,
                                                            Consulta.plano_id == plano_id.id,
                                                            Consulta.data_atendimento >= data_de,
                                                            Consulta.data_atendimento <= data_ate
                                                            )

    return render_template("home.html",
                            filtrovalor=filtrovalor,
                            plano=plano,
                            faturamento=faturamento,
                            data_de=data_de,
                            data_ate=data_ate,
                            form=form,
                            user=current_user)


#ROUTE PARA FUNÇÃO DE DELETAR DADOS (X)
@views.route('/delete-consulta', methods=['POST'])
def delete_note():
    consulta = json.loads(request.data)
    pacienteId = consulta['pacienteId']
    procedimentoId = consulta['procedimentoId']
    planoId = consulta['planoId']
    consultaData = consulta['consultaData']
    consulta = db.session.query(Consulta).filter_by(paciente_id=pacienteId,
                                                    procedimento_id=procedimentoId,
                                                    plano_id=planoId,
                                                    data_atendimento=consultaData).first()
    if consulta:
        if consulta.user_id == current_user.id:
            db.session.delete(consulta)
            db.session.commit()

    return jsonify({})


#ROUTE PARA FUNÇÃO DE FATURAR ($)
@views.route('/faturar-consulta', methods=['POST'])
def faturar_consulta():
    consulta = json.loads(request.data)
    pacienteId = consulta['pacienteId']
    procedimentoId = consulta['procedimentoId']
    planoId = consulta['planoId']
    consultaData = consulta['consultaData']
    consulta = db.session.query(Consulta).filter_by(paciente_id=pacienteId,
                                                    procedimento_id=procedimentoId,
                                                    plano_id=planoId,
                                                    data_atendimento=consultaData).first()
    if consulta:
        if consulta.user_id == current_user.id:
            consulta.faturamento = date.today()
            consulta.pagamento = True
            db.session.add(consulta)
            db.session.commit()

    return jsonify({})


#ROUTE PARA FUNÇÃO DE EDITAR CÉLULAS
@views.route("/update",methods=["POST","GET"])
def update():

        if  request.method == 'POST':
            campo = request.form['campo'] 
            paciente = request.form['paciente']
            procedimento = request.form['procedimento']
            plano = request.form['plano']
            data_atendimento = request.form['data_atendimento']
            value = request.form['value']
            
            if  campo == 'valor':
                consulta = db.session.query(Consulta).filter_by(  user_id=current_user.id,
                                                                    paciente_id=paciente,
                                                                    procedimento_id=procedimento,
                                                                    plano_id=plano,
                                                                    data_atendimento=data_atendimento
                                                                    ).first()
                consulta.valor = value
                db.session.add(consulta)
                db.session.commit()

            success = 1
        return jsonify(success)


#ROUTE MODAL DE CADASTRAR NOVA CONSULTA
@views.route("/novaconsulta",methods=["POST","GET"])
@login_required
def novaconsulta():

    nome = ""
    data_atendimento = ""
    procedimento = ""
    plano = ""

    form = PacienteForm()

    list_plano_saude = db.session.query(Plano)
    form.plano_saude.choices = [(g.id, g.descr) for g in list_plano_saude]

    list_procedimento = db.session.query(Procedimento)
    form.procedimento.choices = [(g.id, g.descr) for g in list_procedimento]

    if form.validate_on_submit():

        nome = form.nome.data
        data_atendimento = form.data_atendimento.data
        procedimento = form.procedimento.data
        plano = form.plano_saude.data

        exist_pac = db.session.query(Paciente).filter_by(nome = nome,user_id=current_user.id).first()

        if exist_pac == None:
                novo_paciente = Paciente(nome=nome,
                                         user_id=current_user.id)
                db.session.add(novo_paciente)
                db.session.commit()

        

        c = Consulta(data_atendimento=data_atendimento)
        c.user = db.session.query(User).filter_by(id=current_user.id).first()
        c.procedimento = db.session.query(Procedimento).filter_by(id=procedimento).first()
        c.plano = db.session.query(Plano).filter_by(id=plano).first()
        c.paciente = db.session.query(Paciente).filter_by(nome = nome).first()

        flash(f'Paciente {c.paciente.nome} atendido(a) dia {c.data_atendimento} pelo plano {c.plano.descr} fez o procedimento {c.procedimento.descr}')

        db.session.add(c)
        db.session.commit()

    return render_template("novaconsulta.html",
                            nome=nome, 
                            data_atendimento=data_atendimento,
                            procedimento=procedimento,
                            plano=plano, 
                            form=form, 
                            user=current_user)

#--------------------------------------------------------------------

#ROUTE PARA CONFIGURAÇÕES

@views.route('/config', methods=['GET', 'POST'])
@login_required
def config():

    planodescr = ""
    procedimentodescr = ""

    procedimentoform = ProcedimentoForm()
    planoform = PlanoForm()

    list_plano_saude = db.session.query(Plano.id, Plano.descr)

    list_procedimento = db.session.query(Procedimento.id, Procedimento.descr)


    #--------------------------------------------------------------------
    # INCLUSÃO DE PROCEDIMENTO


    if procedimentoform.submitprocedimento.data and procedimentoform.validate():

        procedimentodescr = procedimentoform.descr.data

        exist_desc = db.session.query(Procedimento).filter_by(descr = procedimentodescr).first()

        if exist_desc == None:
                novo_procedimento = Procedimento(descr=procedimentodescr)
                db.session.add(novo_procedimento)
                db.session.commit()
                flash(f'Procedimento {novo_procedimento.descr} incluído com sucesso!')

        else:
            flash(f'Procedimento {procedimentodescr} já existe!', category='error')


    #--------------------------------------------------------------------
    # INCLUSÃO DE PLANO


    if planoform.submitplano.data and planoform.validate():

        planodescr = planoform.descr.data

        exist_desc = db.session.query(Plano).filter_by(descr = planodescr).first()

        if exist_desc == None:
                novo_plano = Plano(descr=planodescr)
                db.session.add(novo_plano)
                db.session.commit()
                flash(f'Plano {novo_plano.descr} incluído com sucesso!')

        else:
            flash(f'Plano {planodescr} já existe!', category='error')


    procedimentoform.descr.data = ""
    planoform.descr.data = ""


    
    return render_template("config.html",
                            procedimentoform=procedimentoform,
                            planoform=planoform,
                            procedimento=procedimentodescr,
                            plano=planodescr,
                            list_plano=list_plano_saude,
                            list_procedimento=list_procedimento,
                            user=current_user)


#--------------------------------------------------------------------

#ROUTE PARA PAGINA DE TESTE DE TABELAS

@views.route('/teste', methods=['GET', 'POST'])
@login_required
def teste():

    plano = ""
    faturamento = ""
    data_de = ""
    data_ate = ""

    form = FiltroForm()

    list_plano_saude = db.session.query(Plano)
    form.plano_saude.choices = [(g.id, g.descr) for g in list_plano_saude]

    filtrovalor = db.session.query(Consulta)

    if form.validate_on_submit():

        plano = form.plano_saude.data
        faturamento_form = form.faturamento.data
        data_de = form.data_de.data
        data_ate = form.data_ate.data

        if faturamento_form == "Faturado":
            faturamento = 1
        
        else:
            faturamento = 0

        plano_id = db.session.query(Plano).filter_by(id = plano).first()

        filtrovalor = db.session.query(Consulta).filter(    Consulta.user_id == current_user.id,
                                                            Consulta.pagamento == faturamento,
                                                            Consulta.plano_id == plano_id.id,
                                                            Consulta.data_atendimento >= data_de,
                                                            Consulta.data_atendimento <= data_ate
                                                            )



    return render_template("teste.html",
                            filtrovalor=filtrovalor,
                            plano=plano,
                            faturamento=faturamento,
                            data_de=data_de,
                            data_ate=data_ate,
                            form=form,
                            user=current_user)
