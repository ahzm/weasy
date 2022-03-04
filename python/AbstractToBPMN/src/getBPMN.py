#explicar las bibliotecas
import sys
import json
import random
import string
import os
import requests

from types import SimpleNamespace

from requests.models import Response
from basic_class import *
from partial_order import *
from abstract_graph import *
from bpmn_class import *
from py2pif import *


''' tasks submitted from node js '''
tasks = sys.argv[1]
tasks = json.loads(tasks)

''' links submitted from node js '''
links = sys.argv[2]
links = json.loads(links)

''' nodes submitted from node js '''
nodespy = sys.argv[3]
nodespy = json.loads(nodespy)

# array of activitys pyhton
activitys = []
# array of nodes python
nodess = []
# array of arcs python
arcss = []
# array of sub nodes python
subnodes = []
#array of sub arcs python
subarcs = []

''' URL API '''
url = "http://localhost:8080/transformation/vbpmn/transform/pif2bpmn"

'''Headers for api call'''
headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not;A Brand";v="99", "Microsoft Edge";v="91", "Chromium";v="91"',
    'Accept': '*/*',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41',
    'Origin': 'http://localhost:8080',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'http://localhost:8080/transformation/transform.html',
    'Accept-Language': 'es-419,es;q=0.9,es-ES;q=0.8,en;q=0.7,en-GB;q=0.6,en-US;q=0.5,fr;q=0.4,de;q=0.3'
}
''' rebuild  activitys '''
for task in tasks:
    task["desc"] = ''.join(char for char in task["desc"] if char.isalnum())
    count = 0
    if task["desc"][0].isnumeric():
        task["desc"] = "T"+task["desc"]
    if task["desc"] == "test":
        task["desc"] = task["desc"].upper()
    for element in tasks:
        if element["desc"] == task["desc"]:
            count = count+1
    if count > 1:
        task["desc"] = task["desc"]+"_"+str(tasks.index(task))
    act = Activity(task["desc"].replace(" ", "_"), task["id"],
                   task["dura"][0], task["dura"][1])
    activitys.append(act)



''' rebuild  nodes '''
for nodepy in nodespy:
    n = Node(nodepy["id"])
    for activity in activitys:
        for task in nodepy["list_tasks"]:
            if task["desc"] == activity.get_name():
                n.add_activity(activity)
   # add to array of sub nodes
    if len(nodepy["subgraph"]) > 0:
        sn = nodepy["subgraph"]
        subnodes.append({"node": n, "node_pere": sn[len(sn)-1]})
    else:
        nodess.append(n)

''' rebuild  arcs '''
for link in links:
    # source_node, target_node
    target = link["target"]
    source = link["source"]
    arc = []
    sarc = []
    for nod in nodess:

        if nod.get_ident() == source:
            arc.insert(0, nod)
        elif nod.get_ident() == target:
            arc.insert(1, nod)
    if len(arc) == 2:
        a = Arc(arc[0], arc[1])
        arcss.append(a)
    # checking arcs of sub nodes
    for snod in subnodes:
        if snod["node"].get_ident() == source:
            sarc.insert(0, snod["node"])
            sarc.insert(3, snod["node_pere"])

        elif snod["node"].get_ident() == target:
            sarc.insert(1, snod["node"])
            sarc.insert(3, snod["node_pere"])
    # adding sub arcs
    if len(sarc) >= 2:
        sa = Arc(sarc[0], sarc[1])
        subarcs.append({'subarc': sa, "node_pere": sarc[3]})


''' Function for adding sub nodes and sub arcs to abstract graph '''
def addSubGraphs(temp_nodes):
    for nod in temp_nodes:
        list_Test = list(filter(lambda fille: nod.get_ident()
                                == fille["node_pere"], subnodes))
        list_sa = list(filter(lambda sa: nod.get_ident()
                              == sa["node_pere"], subarcs))
        if len(list_Test) > 0 and len(list_sa) > 0:
            letters = string.ascii_letters
            nod.add_subgraph(SubGraph("subgraph_"+''.join(random.choice(letters) for i in range(6)), [x["node"] for x in list_Test], [
                x['subarc'] for x in list_sa]))

''' checking existance of subnodes'''
if len(subnodes) > 0:
    addSubGraphs(nodess)
    addSubGraphs([n["node"] for n in subnodes])
''' creating BPMN graph'''
BPMNGraph = AbsToBPMNGraph(nodess, arcss)
new_nodes, new_arcs = BPMNGraph.get_BPMN_graph()

''' BPMN to pif'''
pytopif = Py2Pif("py2pif")
directory, name = pytopif.getPIFXML(new_nodes, new_arcs)

'''' open file of pif '''
bpmn = open(directory+'/'+name, 'rb')
'''directory '''
files = [('file1', (name, bpmn.read(), 'application/octet-stream'))]
''' API request and response in string format sending to node '''
response = requests.post(url, headers=headers, files=files)
print(response.text)
sys.stdout.flush()
''' closing pif file '''
bpmn.close()
''' deleting pif file '''
os.remove(directory+'/'+name)
