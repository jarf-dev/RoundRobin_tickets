from functools import reduce
import zendeskUtils
import localUtils

import logging, sys
import configparser

config = configparser.ConfigParser()
config.read('conf.cfg')

logPath = config['database-settings']['LOG_PATH']


logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler(logPath)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)

logger.info('Reinicia ciclo de rutina')


def roundRobin2(idRutina):
    logger.info('hola que hace')

def roundRobin(idRutina):

    try:

        # levanta los datos de la rutina
        rutintaData=localUtils.selectRecordTable('RutinasDisponibles',id=idRutina)[0]

        # vista zendesk asociada a la rutina
        vistaId=rutintaData['idVistaZendesk']

        # obtiene los ticket asignados en la vista de la rutina
        ticketsVista=zendeskUtils.getTicketsOnView(vistaId)

        # si la vista zendesk no tienen ningún ticket termina el proceso
        if len(ticketsVista)==0:
            return

        # agentes zendesk asociados a la rutina
        agentesRutina=localUtils.selectRecordTable('CargaAgentes',idRutina=idRutina)

        # considera sólo agentes con estado activo
        agentesActivos=[agente for agente in agentesRutina if agente['esActivado']==1]

        # revisa si hay un turno asignado
        marcadorTurnos=[agente['marcadorTurno'] for agente in agentesActivos]
        result=reduce((lambda a, b: a + b), marcadorTurnos)
        
        # si no hay turno lo asigna
        if result==0:
            agentesActivos[0]['marcadorTurno']=1

        for idAgente, agente in enumerate(agentesActivos):
            if agente['marcadorTurno']==1:
                break

    except Exception as err:
        logger.error(f'Ha ocurrido un error: {err}')

    for ticket in ticketsVista:
        
        try:
            # asignación_equitativa_ejecutada
            idTicket=ticket['id']
            idZendeskAgente=agentesActivos[idAgente]['idAgenteZendesk']
            zendeskUtils.assignTicket(ticket['id'],agentesActivos[idAgente]['idAgenteZendesk'],'asignacion_equitativa_ejecutada')
            logger.info(f'rutina: {idRutina}. ticket {idTicket} fue asignado al agente {idZendeskAgente}')
            localUtils.updateRecordTable('CargaAgentes',id=agentesActivos[idAgente]['id'],marcadorTurno=0)
            idAgente=loopId(idAgente,len(agentesActivos))
            localUtils.updateRecordTable('CargaAgentes',id=agentesActivos[idAgente]['id'],marcadorTurno=1)
        except Exception as err:
            logger.error(f'Error al asignar ticket {idTicket}: {err}')



# función que cambia el id del arreglo
def loopId(id,maxElem):
    if id==maxElem-1:
        nextId=0
    else:
        nextId=id+1
    
    return nextId

if __name__=="__main__":
    pass