''' Program to get the initial abstract graph  '''
import sys
import json
import ast
from types import SimpleNamespace
from basic_class import *
from partial_order import *
from abstract_graph import *
from bpmn_class import *

''' tasks submitted from node js '''
tasks = sys.argv[1]
tasks = json.loads(tasks)
''' couples submitted from node js '''
couples = sys.argv[2]
couples = json.loads(couples)

activitys = []
op = []

'''Formating tasks in activitys object'''
def get_tasks(tasks):
    arr_activitys = []
    for task in tasks:
        act = Activity(task["id"], task["desc"],
                       task["dura"][0], task["dura"][1])
        arr_activitys.append(act)
    return arr_activitys


''' Formatting couples in couples array  '''

def get_couples(couples):
    # partial order
    op = []
    for couple in couples:
        arr_couple = []
        for acti in activitys:
            if acti.get_ident() == couple[0]:
                arr_couple.insert(0, acti)
            if acti.get_ident() == couple[1]:
                arr_couple.insert(1, acti)
        op.append(arr_couple)
    return op

''' calling partial order '''
activitys = get_tasks(tasks)
op = get_couples(couples)
op_obj = PartialOrder(activitys, op)
abs_nodes, abs_arcs = op_obj.generate_abstract_model()
arr_nodes = []
arr_arcs = []

''' formatting arcs in Arcs dict'''
def get_arcs(abs_arcs):
    arr_arcs = []
    for abs_arc in abs_arcs:
        obj = {
            "ident": abs_arc.get_ident(),
            "source_node": abs_arc.get_source_node().get_ident(),
            "target_node": abs_arc.get_target_node().get_ident()
        }
        arr_arcs.append(obj)
    return arr_arcs

''' formating and making object for nodes'''

def get_nodes(abs_nodes):
    arr_nodes = []
    for abs_node in abs_nodes:
        la = []
        sub = {}
        temp_nodes = []
        temp_arcs = []
        for acty in abs_node.get_list_activities():
            la.append(acty.get_ident())
        if abs_node.get_subgraphs():
            # {subgraph_key:[[nodes],[arcs]]}
            for graph in abs_node.get_subgraphs().values():
                sub['nodes'] = get_nodes(graph[0])
                sub['arcs'] = get_arcs(graph[1])
      
        obj = {
            "ident": abs_node.get_ident(),
            "list_activities": la,
            "subgraph": sub
        }
        arr_nodes.append(obj)
    return arr_nodes


arr_nodes = get_nodes(abs_nodes)


'''Making object abstract graph and sending response in dict format to node '''
arr_arcs = get_arcs(abs_arcs)
abstractGraph = AbstractGraph(abs_nodes, abs_arcs)
minTime = abstractGraph.get_min_time()
maxTime = abstractGraph.get_max_time()
obj = {
    "nodes": arr_nodes,
    "arcs": arr_arcs,
    "minTime": minTime,
    "maxTime": maxTime
}
print(json.dumps(obj))
sys.stdout.flush()
