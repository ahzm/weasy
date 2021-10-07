#/usr/bin/env python3
# -*- coding:utf-8 -*-
# author: ahzm
# update: Jan 05, 2021

"""
BPMN module: 
Mainly contains: 1) AbsToBPMNGraph class, 2)BPMN class
"""

from basic_class import *
from abstract_graph import *

class BPMNNode:
    def __init__(self, ident):
         self.ident = ident
         
    def get_ident(self):
        return self.ident

class Start(BPMNNode):

    def __init__(self,ident):
        self.ident = ident
        self.list_activites = []
        self.subgraphs = {}

    def get_ident(self):
        return self.ident
    
    def get_subgraphs(self):
        return self.subgraphs
    
    def get_list_activities(self):
        return self.list_activites

class End(BPMNNode):
    countEnd=0
    def __init__(self,ident):
        self.ident = ident+str(End.countEnd)
        self.list_activites = []
        self.subgraphs = {}
        End.countEnd+=1

    def get_ident(self):
        return self.ident
    
    def get_list_activities(self):
        return self.list_activites

    def get_subgraphs(self):
        return self.subgraphs

class ExcluNode(BPMNNode):

    countExclu = 0
    def __init__(self, ident):
        self.ident = ident + str(ExcluNode.countExclu)
        self.list_activites = []
        self.subgraphs = {}
        ExcluNode.countExclu += 1
        
    def get_ident(self):
        return self.ident
    
    def get_list_activities(self):
        return self.list_activites

    def get_subgraphs(self):
        return self.subgraphs

class ParalNode(BPMNNode):
    
    count = 0
    def __init__(self, ident):
        self.ident = ident + str(ParalNode.count)
        self.list_activites = []
        self.subgraphs = {}
        ParalNode.count +=1

    def get_ident(self):
        return self.ident

    def get_list_activities(self):
        return self.list_activites

    def get_subgraphs(self):
        return self.subgraphs

class AbsToBPMNGraph(AbstractGraph):
    
    def __init__(self, nodes, arcs):
        self.nodes            = nodes
        self.arcs             = arcs
        self.dict_precu_graph = super().generate_dict_precu_graph()
        self.dict_succ_graph  = super().generate_dict_succ_graph()
        self.start_node       = super().get_start_node()

    def get_dict_precu_graph(self):
        return self.dict_precu_graph
    
    def get_dict_succ_graph(self):
        return self.dict_succ_graph
    
    def add_node(self, node):
        self.nodes.append(node)

    def add_arc(self, arc):
        self.arcs.append(arc)    
    
    def add_arc_nodes(self, source_node, target_node):
        #new_arc = Arc(source_node, target_node)
        self.add_arc(Arc(source_node, target_node))

    def transfor_subgraph(self, nodes, arcs):
        """
        Get the first element and the last element in the subgraph
        """
        dict_succ_graph = {}
        dict_precu_graph = {}
        for node in nodes: 
            dict_precu_graph.setdefault(node, [])
            dict_succ_graph.setdefault(node,[])
            for arc in arcs:
                if(node == arc.get_target_node()):
                    dict_precu_graph.setdefault(node, []).append(arc.get_source_node())
                if(node == arc.get_source_node()):
                    dict_succ_graph.setdefault(node, []).append(arc.get_target_node())
        for node in nodes: 
            if dict_precu_graph[node] == []:
                first_element = node
            if dict_succ_graph[node] == []:
                last_element = node
        return first_element, last_element

    def transfor_all_nodes(self, subnodes=[], subarcs=[]):
        bpmn_nodes = []
        bpmn_arcs  = []
        nodes = []
        arcs =  []
        dict_succ_graph = {}
        dict_precu_graph = {}

        if subnodes and subarcs:
            nodes = subnodes[:]
            arcs  = subarcs[:]
            for node in nodes: 
                dict_precu_graph.setdefault(node, [])
                dict_succ_graph.setdefault(node,[])
                for arc in arcs:
                    if(node == arc.get_target_node()):
                        dict_precu_graph.setdefault(node, []).append(arc.get_source_node())
                    if(node == arc.get_source_node()):
                        dict_succ_graph.setdefault(node,[]).append(arc.get_target_node())

            #print('succ:', dict_succ_graph)
            #print('precu:', dict_precu_graph)
            subgraph_end_nodes = AbstractGraph(subnodes, subarcs).get_end_node()

        else:
            nodes = self.nodes[:]
            arcs  = self.arcs[:]
            dict_succ_graph = self.dict_succ_graph
            dict_precu_graph = self.dict_precu_graph   
        #print('succ:', dict_succ_graph)
        #print('precu:', dict_precu_graph)
        for key_node, succ_nodes in dict_succ_graph.items():
            if not subnodes and not subarcs:
                if(len(succ_nodes) == 0):
                    #print('end', key_node.get_ident())   
                    end_node = End('end')
                    nodes.append(end_node)
                    arcs.append(Arc(key_node, end_node))
            
            if(len(succ_nodes) >= 2):
                exclu_node = ExcluNode('exclusive_split')
                nodes.append(exclu_node)
                for arc in arcs:
                    if arc.get_source_node() == key_node:
                        arc.set_source_node(exclu_node)
                arcs.append(Arc(key_node, exclu_node))

        for key_node, precu_nodes in dict_precu_graph.items():
            if not subnodes and not subarcs:
                if(len(precu_nodes) == 0):
                    #print('key_node', key_node.get_ident())
                    start_node = Start('start')
                    nodes.append(start_node)
                    arcs.append(Arc(start_node, key_node))

            if(len(precu_nodes) >= 2):
                exclu_node = ExcluNode('exclusive_merge')
                nodes.append(exclu_node)
                for arc in arcs:
                    if arc.get_target_node() == key_node:
                        arc.set_target_node(exclu_node)
                arcs.append(Arc(exclu_node, key_node))
                #print(arcs)

        if subnodes and subarcs:
            #print([arc.get_ident() for arc in subarcs])
            if len(subgraph_end_nodes) >= 2:
                exclu_node = ExcluNode('exclusive_merge')
                nodes.append(exclu_node)
                for end_node in subgraph_end_nodes:
                    #print('end_node_:',end_node.get_ident())
                    arcs.append(Arc(end_node, exclu_node))

        # print([arc.get_ident() for arc in arcs])
        # print([node.get_ident() for node in nodes])
        dict_nodes = {}
        for node in nodes:
            if node.get_list_activities() and not node.get_subgraphs():
                if len(node.get_list_activities()) == 1:
                    dict_node = {}
                    dict_node['first'] = node.get_list_activities()[0]
                    dict_node['last'] = node.get_list_activities()[0]
                    dict_node['elements'] = [node.get_list_activities()[0]]
                    dict_node['arcs'] = []
                    dict_nodes[node] = dict_node
                    #print(dict_nodes[node]['first'])

                if len(node.get_list_activities()) >= 2:
                    dict_node = {}
                    start_parallel = ParalNode('start_parallel')
                    end_parallel   = ParalNode('end_parallel')
                    dict_node['first'] = start_parallel
                    dict_node['last'] = end_parallel
                    nodes_elements = []
                    nodes_elements_arcs = []
                    nodes_elements.extend(node.get_list_activities())
                    nodes_elements.append(start_parallel)
                    nodes_elements.append(end_parallel)
                    for activ in node.get_list_activities():
                        nodes_elements_arcs.append(Arc(start_parallel, activ))
                        nodes_elements_arcs.append(Arc(activ, end_parallel))
                    dict_node['elements'] = nodes_elements
                    dict_node['arcs'] = nodes_elements_arcs
                    #print(dict_node)
                    dict_nodes[node] = dict_node
                    #print(dict_nodes[node]['first'])
            elif not node.get_list_activities() and node.get_subgraphs():
                if len(node.get_subgraphs()) == 1:
                    #print('yes')
                    dict_node = {}
                    for subgraph in node.get_subgraphs():
                        b_nodes, b_arcs = self.transfor_all_nodes(node.get_subgraphs()[subgraph][0], node.get_subgraphs()[subgraph][1])
                        #print(b_nodes, [arc.get_ident() for arc in b_arcs])
                        first_element, last_element = self.transfor_subgraph(b_nodes, b_arcs)
                        #print(first_element, last_element)
                    dict_node['first'] = first_element
                    dict_node['last'] = last_element
                    dict_node['elements'] = b_nodes
                    dict_node['arcs'] = b_arcs
                    dict_nodes[node] = dict_node

                if len(node.get_subgraphs()) >= 2:
                    dict_node = {}
                    start_parallel = ParalNode('start_parallel')
                    end_parallel   = ParalNode('end_parallel')
                    dict_node['first'] = start_parallel
                    dict_node['last'] = end_parallel
                    nodes_elements = []
                    nodes_elements_arcs = []
                    for subgraph in node.get_subgraphs():
                        b_nodes, b_arcs = self.transfor_all_nodes(node.get_subgraphs()[subgraph][0], node.get_subgraphs()[subgraph][1])
                        #print("b_nodes, b_arcs :", b_nodes, [arc.get_ident() for arc in b_arcs])
                        first_element, last_element = self.transfor_subgraph(b_nodes, b_arcs)
                        #print(first_element, last_element)
                        nodes_elements.extend(b_nodes)
                        nodes_elements_arcs.extend(b_arcs)
                        nodes_elements_arcs.append(Arc(start_parallel, first_element))
                        nodes_elements_arcs.append(Arc(last_element, end_parallel))
                    dict_node['elements'] = nodes_elements
                    dict_node['arcs'] = nodes_elements_arcs
                    dict_nodes[node] = dict_node

            elif node.get_list_activities() and node.get_subgraphs():
                    dict_node = {}
                    start_parallel = ParalNode('start_parallel')
                    end_parallel   = ParalNode('end_parallel')
                    dict_node['first'] = start_parallel
                    dict_node['last'] = end_parallel
                    nodes_elements = []
                    nodes_elements_arcs = []

                    nodes_elements.extend(node.get_list_activities())
                    nodes_elements.append(start_parallel)
                    nodes_elements.append(end_parallel)
                    for activ in node.get_list_activities():
                        nodes_elements_arcs.append(Arc(start_parallel, activ))
                        nodes_elements_arcs.append(Arc(activ, end_parallel))

                    for subgraph in node.get_subgraphs():
                        b_nodes, b_arcs = self.transfor_all_nodes(node.get_subgraphs()[subgraph][0], node.get_subgraphs()[subgraph][1])
                        first_element, last_element = self.transfor_subgraph(b_nodes, b_arcs)
                        nodes_elements.extend(b_nodes)
                        nodes_elements_arcs.extend(b_arcs)
                        nodes_elements_arcs.append(Arc(start_parallel, first_element))
                        nodes_elements_arcs.append(Arc(last_element, end_parallel))
                    dict_node['elements'] = nodes_elements
                    dict_node['arcs'] = nodes_elements_arcs
                    dict_nodes[node] = dict_node
                
            else:
                dict_node = {}
                dict_node['first'] = node
                dict_node['last'] = node
                dict_node['elements'] = [node]
                dict_node['arcs'] = []
                dict_nodes[node] = dict_node
                    
        #print([arc.get_ident() for arc in arcs])
        #print([node.get_ident() for node in nodes])
        for node in nodes:
            bpmn_nodes.extend(dict_nodes[node]['elements'])
            bpmn_arcs.extend(dict_nodes[node]['arcs'])
            for arc in arcs:
                if arc.get_source_node() == node:
                    bpmn_arcs.append(Arc(dict_nodes[node]['last'], dict_nodes[arc.get_target_node()]['first']))

        return bpmn_nodes, bpmn_arcs

    def get_BPMN_graph(self):
        bpmn_nodes, bpmn_arcs = self.transfor_all_nodes()
        return bpmn_nodes, bpmn_arcs

class BPMNGraph:

    def __init__(self, nodes, arcs):
        self.nodes = nodes
        self.arcs = arcs
    
    def add_node(self, new_node):
        self.nodes.append(new_node)

    def add_arc(self, new_arc):
        self.arcs.append(new_arc)

    def get_nodes(self):
        return self.nodes
    
    def get_arcs(self):
        return self.arcs