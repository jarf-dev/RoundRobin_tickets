import os
import json
from datetime import datetime

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

from requests.models import HTTPError

import zendeskUtils
import localUtils

# Instantiation
app = Flask(__name__)

# Settings
CURRENT_DIR=os.getcwd()
CORS(app, resources={r"/*": {"origins": "*"}})

# Routes
@app.route('/')

# Load angular frontend
def index():
    return render_template('index.html')

@app.route('/zendesk/agentes', methods=['GET'])
def agentesZendesk():
    if request.method =='GET':
        results=zendeskUtils.getZendeskUsers()

        return results

@app.route('/zendesk/vistas', methods=['GET'])
def vistasZendesk():
    if request.method =='GET':
        results=zendeskUtils.getZendeskViews()

        return results

@app.route('/zendesk/manage-tickets/<id>', methods=['PUT'])
def manageTicketsZendesk(id):
    if request.method =='PUT':
        try:
            agenteId=request.json['id_agente']
            tags=request.json['tags_adicionales']

            zendeskResponse=zendeskUtils.assignTicket(id,agenteId,*tags)

            if zendeskResponse.status_code == 200:
                message = {
            'message': 'Update data successfully done',
            'details': f'Ticket: {id} asignado al agente {agenteId}'
            }
            else:
                message=zendeskResponse.text
            
            response_code=zendeskResponse.status_code

        except HTTPError:
            message = {
            'message': 'Bad request specification: not enough params defined'
            }
            response_code=400

        response = jsonify(message)
        response.status_code = response_code
        return response

@app.route('/local/rutinas-disponibles',methods=['GET','POST'])
def globalRutinasDisponibles():
    if request.method =='GET':
        # levanta parámetros para filtros
        if request.args.get("TotAgentes")=='1':
            return json.dumps(localUtils.selectRecordTable('RutinasDisponiblesTotAgentes'))
        else:
            return json.dumps(localUtils.selectRecordTable('RutinasDisponibles'))

    if request.method =='POST':

        try:
            diaHoy=datetime.today().strftime('%d-%m-%Y')
            extraArgs=f'{{"ultimoCambioEstado":"{diaHoy}","esActivado":1}}'
            extraArgsJson=json.loads(extraArgs)

            mergedArgs={**extraArgsJson,**request.json}

            new_id=localUtils.insertRecordTable('RutinasDisponibles',**mergedArgs)

            message = {
            'message': 'Insert data successfully done',
            'new_id':new_id
            }
            response_code=200

        except HTTPError:
            message = {
            'message': 'Bad request specification: not enough params defined'
            }
            response_code=400

        response = jsonify(message)
        response.status_code = response_code
        return response

@app.route('/local/rutinas-disponibles/<id>',methods=['GET','PUT','DELETE'])
def indivRutinasDisponibles(id):
    if request.method =='GET':
        # levanta parámetros para filtros
        results=json.dumps(localUtils.selectRecordTable('RutinasDisponibles',id))
        return results

    if request.method =='PUT':
        try:
            localUtils.updateRecordTable('RutinasDisponibles',id,**request.json)
            message = {
            'message': 'Update data successfully done'
            }
            response_code=200

        except HTTPError:
            message = {
            'message': 'Bad request specification: not enough params defined'
            }
            response_code=400

        response = jsonify(message)
        response.status_code = response_code
        return response

    if request.method =='DELETE':
        # borrar usando parametros
        try:
            # levanta parámetros para filtros
            if request.args.get("tipo")=='Todo':
                localUtils.deleteRecordTable('CargaAgentes',id,all=True)
                localUtils.deleteRecordTable('RutinasDisponibles',id)
                message = {
                'message': 'Delete data successfully done'}
            if request.args.get("tipo")=='SoloAgentes':
                localUtils.deleteRecordTable('CargaAgentes',id,all=True)
                message = {
                'message': 'Delete data successfully done'}
            else:
                localUtils.deleteRecordTable('RutinasDisponibles',id)
                message = {
                'message': 'Delete data successfully done'}
            
            response_code=200

        except HTTPError:
            message = {
            'message': 'Bad request specification: not enough params defined'
            }
            response_code=400

        response = jsonify(message)
        response.status_code = response_code
        return response

@app.route('/local/carga-agentes',methods=['GET','POST'])
def globalCargaAgentes():
    if request.method =='GET':
        # levanta parámetros para filtros
        results=json.dumps(localUtils.selectRecordTable('CargaAgentes'))
        return results

    if request.method =='POST':

        try:
            localUtils.insertRecordTable('CargaAgentes',**request.json)

            message = {
            'message': 'Insert data successfully done'
            }
            response_code=200

        except HTTPError:
            message = {
            'message': 'Bad request specification: not enough params defined'
            }
            response_code=400

        response = jsonify(message)
        response.status_code = response_code
        return response

@app.route('/local/carga-agentes/<id>',methods=['GET','PUT','DELETE'])
def indivCargaAgentes(id):
    if request.method =='GET':
        # levanta parámetros para filtros
        if request.args.get("DetalleZendesk")=='1':
            agentesRutina=localUtils.selectRecordTable('CargaAgentes',idRutina=id)
            agentesZendesk=json.loads(zendeskUtils.getZendeskUsers())

            for agente in agentesRutina:
                extra=[x for x in agentesZendesk if str(x["idZendesk"])==str(agente["idAgenteZendesk"])][0]
                agente["nombre"]=extra["nombre"]
                agente["email"]=extra["email"]
                agente["idZendesk"]=extra["idZendesk"]
                agente["tipoOrigen"]="DB"

            results= json.dumps(list(agentesRutina))

        else:
            results=json.dumps(localUtils.selectRecordTable('CargaAgentes',idRutina=id))
        return results

    if request.method =='PUT':
        try:
            localUtils.updateRecordTable('CargaAgentes',id,**request.json)
            message = {
            'message': 'Update data successfully done'
            }
            response_code=200

        except HTTPError:
            message = {
            'message': 'Bad request specification: not enough params defined'
            }
            response_code=400

        response = jsonify(message)
        response.status_code = response_code
        return response

    if request.method =='DELETE':
        # borrar usando parametros
        try:
            localUtils.deleteRecordTable('CargaAgentes',id)
            message = {
            'message': 'Delete data successfully done'
            }
            response_code=200

        except HTTPError:
            message = {
            'message': 'Bad request specification: not enough params defined'
            }
            response_code=400

        response = jsonify(message)
        response.status_code = response_code
        return response


@app.route('/local/algoritmos',methods=['GET'])
def globalAlgoritmos():
    if request.method =='GET':
        # levanta parámetros para filtros
        results=json.dumps(localUtils.selectRecordTable('AlgoritmosDisponibles'))
        return results

# Despliega error si el recurso no es encontrado
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

if __name__ == "__main__":
    app.run()