# website/rasaweb/utils/service_now.py
# __author__='Lokesh Kuncham'

import requests
import ast
session = requests.Session()
session.auth = ("admin", "ic+!K8Ae4PhI")
base_url = "https://dev116021.service-now.com/api/"
create_incident = "now/table/incident"
get_incident = "now/v1/table/incident?sysparm_query=number="


def create_ticket(short_description="Default Description",description="Default Description"):
    json_paylod = {"short_description": short_description, "description": description}
    response = session.post(base_url+create_incident,json=json_paylod)
    return response.json()
#create_ticket()

def get_ticket_details(ticket_id):
    response = session.get(base_url+get_incident+ticket_id)
    return response.json()

get_ticket_details("INC0010022")

