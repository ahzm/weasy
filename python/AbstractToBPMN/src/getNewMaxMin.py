''' Program to get the compute time of the abstract graph '''
import sys
import json
import random
import string
from types import SimpleNamespace
from basic_class import *
from partial_order import *
from abstract_graph import *
from bpmn_class import *

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

''' rebuild  activitys '''
for task in tasks:
    act = Activity(task["desc"], task["id"], task["dura"][0], task["dura"][1])
    activitys.append(act)

''' rebuild  nodes '''
for nodepy in nodespy:
    n = Node(nodepy["id"])
    for activity in activitys:
        for task in nodepy["list_tasks"]:
            if task["id"] == activity.get_ident() and task["desc"] == activity.get_name():
                n.add_activity(activity)
   # add to array of sn
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
    for snod in subnodes:
        if snod["node"].get_ident() == source:
            sarc.insert(0, snod["node"])
            sarc.insert(3, snod["node_pere"])

        elif snod["node"].get_ident() == target:
            sarc.insert(1, snod["node"])
            sarc.insert(3, snod["node_pere"])
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

''' Creating abstract graph'''
abgraph = AbstractGraph(nodess, arcss)

''' Object for max time and min time of the graph '''
obj = {
    "minTime": abgraph.get_min_time(),
    "maxTime": abgraph.get_max_time()
}
''' Sending object to node '''
print(json.dumps(obj))
sys.stdout.flush()
