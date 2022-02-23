import os, json

import requests

from dotenv import load_dotenv
load_dotenv()

from auxiliar import *

import configparser

config = configparser.ConfigParser()
config.read('conf.cfg')

zendeskAccount = config['zendesk-setting']['ZENDESK_ACCOUNT']

# establece la string de autentificación
USER=os.getenv("USER_EMAIL")
API_TOKEN=os.getenv("API_TOKEN")
authString="Basic "+string2encode64(f"{USER}/token:{API_TOKEN}")

# envia una solicitud tipo GET a la API de zendesk
def getZendesk(url):
    URL=f'{zendeskAccount}/api/v2/{url}'
    HEADERS={
        "content-type": "application/json",
        "Authorization": authString
    }
    response = requests.get(URL,headers=HEADERS)
    return response.json()

# envia una solicitud tipo PUT a la API de zendesk
def putZendesk(url,data):
    URL=f'{zendeskAccount}/api/v2/{url}'
    HEADERS = {
        "content-type": "application/json",
        "Authorization": authString
    }
    response = requests.put(URL,data=data,headers=HEADERS)
    return response

# devuelve un listado de todos los agentes activos en la cuenta zendesk
def getZendeskUsers():
    
    userList=[]
    
    url="users.json?role[]=admin&role[]=agent"

    while True:    
        respZendesk=getZendesk(url)

        for user in respZendesk['users']:

            userZendesk={
                    'nombre':user['name'],
                    'email':user['email'],
                    'idZendesk':user['id']
                }

            userList.append(userZendesk)
           
        if respZendesk['next_page']:
            url=respZendesk['next_page']
        else:
            break

    return json.dumps(userList)

# devuelve un listado de las vistas activas en la cuenta zendesk
def getZendeskViews():

    viewList=[]
    url="views"

    while True:
        respZendesk=getZendesk(url)

        for view in respZendesk['views']:
            viewZendesk={
                'title':view['title'],
                'idZendesk':view['id'],
                'url':view['url'],
                'active':view['active']
            }

            viewList.append(viewZendesk)

        if respZendesk['next_page']==None:
            break 
        else:
            url=respZendesk['next_page'][respZendesk['next_page'].find("views"):] 

    return json.dumps(viewList)

# Función que asigna un ticket a un determinado usuario
def assignTicket(ticketId,agentId,*args):

    data=f"""
        {{"ticket":{{
            "assignee_id":{agentId},
            "additional_tags":[
                {",".join('"'+str(e)+'"' for e in args)}
            ]
        }}
        }}
    """
    zendeskResponse=putZendesk(f"tickets/update_many.json?ids={ticketId}",data)

    return zendeskResponse

# devuelve un listado de los tickets en las vistas activas en la cuenta zendesk
def getTicketsOnView(viewId):
    ticketList=[]
    url=f"views/{viewId}/tickets.json"
    
    while True:    
        respZendesk=getZendesk(url)

        for ticket in respZendesk['tickets']:

            ticketZendesk={
                    'id':ticket['id']
                }

            ticketList.append(ticketZendesk)
           
        if respZendesk['next_page']:
            url=respZendesk['next_page'][respZendesk['next_page'].find("views"):]
        else:
            break

    return ticketList