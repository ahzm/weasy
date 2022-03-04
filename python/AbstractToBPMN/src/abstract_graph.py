# /usr/bin/env python3
# -*- coding:utf-8 -*-
# author: ahzm
# update: March 29, 2021

"""
Abstract Graphe module : AbstractGraph class, SubGraph class
"""
from basic_class import *


class AbstractGraph:

    def __init__(self, nodes, arcs):

        self.nodes = nodes
        self.arcs = arcs
        self.dict_succ_graph = self.generate_dict_succ_graph()
        self.dict_precu_graph = self.generate_dict_precu_graph()
        self.add_succ_node()
        self.start_node = self.get_start_node()
        self.dict_compte_min = self.init_dict_compte_min()
        self.dict_compte_max = self.init_dict_compte_max()

    def init_dict_compte_min(self):
        dict_compte_min = {}
        for node in self.nodes:
            dict_compte_min[node] = 0
        return dict_compte_min

    def init_dict_compte_max(self):
        dict_compte_max = {}
        for node in self.nodes:
            dict_compte_max[node] = 0
        return dict_compte_max

    def add_arc(self, arc):
        self.arcs.append(arc)

    def add_arcs(self, *arcs):
        self.arcs.extend(arcs)

    def add_node(self, node):
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes

    def get_arcs(self):
        return self.arcs

    def add_succ_node(self):
        for node in self.dict_succ_graph.keys():
            node.succ_nodes.extend(self.dict_succ_graph[node])

    def generate_dict_succ_graph(self):
        succ_graph = {}
        for node in self.nodes:
            succ_graph.setdefault(node, [])
            for arc in self.arcs:
                if (node == arc.get_source_node()):
                    succ_graph.setdefault(node, []).append(
                        arc.get_target_node())
        return succ_graph

    def get_dict_succ_graph(self):
        return self.generate_dict_succ_graph()

    def generate_dict_precu_graph(self):
        precu_graph = {}
        for node in self.nodes:
            precu_graph.setdefault(node, [])
            for arc in self.arcs:
                if(node == arc.get_target_node()):
                    precu_graph.setdefault(node, []).append(
                        arc.get_source_node())
        return precu_graph

    def get_dict_precu_graph(self):
        return self.generate_dict_succ_graph()

    def graph_connect(self):  # XXX
        """Determine whether the graph is connected"""
        list_nodes = []

        for node in self.nodes:
            list_nodes.append(node)

        for arc in self.arcs:
            # if not list_nodes: return True
            if arc.get_source_node() in list_nodes:
                list_nodes.remove(arc.get_source_node())
            if arc.get_target_node() in list_nodes:
                list_nodes.remove(arc.get_target_node())

        if len(list_nodes):
            print('list_nodes : ', [node for node in list_nodes])
        else:
            print("--Ok. Graph is connected.--")
        return (len(list_nodes) == 0)

    def isCycleUtil(self, node, resStack):
        resStack[node] = True
        for succ_node in self.dict_succ_graph[node]:
            if resStack[succ_node] == False:
                if self.isCycleUtil(succ_node, resStack) == True:
                    return True
            elif resStack[succ_node] == True:
                return True

    def isCycle(self):
        resStack = {}
        for node in self.nodes:
            resStack[node] = False
        for node in self.nodes:
            if self.isCycleUtil(node, resStack) == True:
                return True
            else:
                return False
        return False

    def print_isCycle(self):
        if self.isCycle == True:
            print('Graph has a cycle')
        else:
            print('Gaphe has no cycle')

    def dfs(self, node_index, visited, trace, results):
        if (node_index in visited):
            if (node_index in trace):
                trace_index = trace.index(node_index)
                result = []
                for i in range(trace_index, len(trace)):
                    #print(trace[i] + ' ', end='')
                    result.append(trace[i])
                #print('\n', end='')
                results.append(result)
                return
            return
        visited.append(node_index)
        trace.append(node_index)
        if(node_index):
            children = self.dict_succ_graph[node_index]
            for child in children:
                self.dfs(child, visited, trace, results)
        trace.pop()

    def get_all_cycles(self):
        visited = []
        trace = []
        results = []
        self.dfs(self.get_start_node(), visited, trace, results)
        return results

    def get_temps_cycles(self):
        temp_cycles = []
        for result in results:
            temp_max = 0
            for node in result:
                temp_max += node.calcule_max_time()
            temp_cycles.append(temp_max)
        return temp_cycles

    def set_start_node(self, new_start_node):
        self.start_node = new_start_node

    def get_start_node(self):
        for key in self.dict_precu_graph.keys():
            if self.dict_precu_graph[key] == []:
                return key

    def get_end_node(self):
        end_nodes = []
        self.dict_succ_graph = self.generate_dict_succ_graph()
        for key in self.dict_succ_graph.keys():
            if self.dict_succ_graph[key] == []:
                end_nodes.append(key)
        return end_nodes

    def add_nullnode(self, first_node, second_node, _type=0):  # FIXME
        """exclusive"""
        start_nullnode = NullNode('start_node')
        end_nullnode = NullNode('end_node')
        self.add_node(start_nullnode)
        self.add_node(end_nullnode)
        arc_null_first_node = Arc(start_nullnode, first_node)
        arc_null_second_node = Arc(start_nullnode, second_node)
        arc_first_node_null = Arc(first_node, end_nullnode)
        arc_second_node_null = Arc(second_node, end_nullnode)
        self.add_arcs(arc_null_first_node)
        self.add_arcs(arc_null_second_node)
        self.add_arcs(arc_first_node_null)
        self.add_arcs(arc_second_node_null)
        self.set_start_node(start_nullnode)

    def calcule_max_time(self, start_node=None):

        if not start_node:
            start_node = self.start_node

        if not start_node.succ_nodes:
            return start_node.calcule_max_time()
        else:
            max_time = 0
            for succ_node in start_node.succ_nodes:
                self.dict_compte_max[succ_node] += 1
                if self.dict_compte_max[succ_node] > 1:
                    #print(succ_node.get_ident())
                    for succ_node_temp in succ_node.succ_nodes:
                        #self.dict_compte_max[succ_node_temp] -= 1
                        if self.dict_compte_max[succ_node_temp] < 2:
                            tmp_max_time = self.calcule_max_time(
                                succ_node_temp)
                            max_time = max(tmp_max_time, max_time)
                            return max_time
                    continue
                else:
                    tmp_max_time = self.calcule_max_time(succ_node)
                    max_time = max(tmp_max_time, max_time)
            return start_node.calcule_max_time() + max_time

    def calcule_min_time(self, start_node=None):
        #print('start node', start_node)
        if not start_node:
            start_node = self.start_node

        if not start_node.succ_nodes:
            return start_node.calcule_min_time()
        else:
            min_time = float('inf')
            for succ_node in start_node.succ_nodes:
                self.dict_compte_min[succ_node] += 1
                if self.dict_compte_min[succ_node] <= 1:
                    tmp_min_time = self.calcule_min_time(succ_node)
                    min_time = min(tmp_min_time, min_time)
            return start_node.calcule_min_time() + min_time

    def get_min_time(self):
        #print('Min time:')
        return self.calcule_min_time()

    def get_max_time(self):
        #print('Max time:')
        return self.calcule_max_time()


class SubGraph(AbstractGraph):

    def __init__(self, ident, nodes, arcs):

        self.ident = ident
        self.nodes = nodes
        self.arcs = arcs
        self.dict_succ_graph = super().generate_dict_succ_graph()
        self.dict_precu_graph = super().generate_dict_precu_graph()
        self.start_node = super().get_start_node()
        super().add_succ_node()
        self.dict_compte_min = super().init_dict_compte_min()
        self.dict_compte_max = super().init_dict_compte_max()

    def get_ident(self):
        return self.ident
