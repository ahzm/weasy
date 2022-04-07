# /usr/bin/env python3
# -*- coding:utf-8 -*-
# author: Ahang
# update: March 29, 2021

"""
Basic class module: Activity class, Arc class and Node class.
"""

from abstract_graph import SubGraph


class Activity:
    """Activity class"""

    def __init__(self, ident, name, min_execu_time, max_execu_time):

        self.ident = str(ident)
        self.name = str(name)
        self.min_execu_time = min_execu_time
        self.max_execu_time = max_execu_time

    def set_ident(self, new_ident):
        self.ident = str(new_ident)

    def get_ident(self):
        return self.ident

    def set_name(self, new_name):
        self.name = str(new_name)

    def get_name(self):
        return self.name

    def set_min_execu_time(self, new_min_execu_time):
        self.min_execu_time = new_min_execu_time

    def get_min_execu_time(self):
        return self.min_execu_time

    def set_max_execu_time(self, new_max_execu_time):
        self.max_execu_time = new_max_execu_time

    def get_max_execu_time(self):
        return self.max_execu_time


class Arc:
    "Arc class"

    def __init__(self, source_node, target_node):
        self.ident = str(source_node.get_ident()) + "-" + \
            str(target_node.get_ident())
        self.source_node = source_node
        self.target_node = target_node

    def set_ident(self, new_ident):
        self.ident = new_ident

    def get_ident(self):
        return self.ident

    def set_source_node(self, new_source_node):
        self.source_node = new_source_node

    def get_source_node(self):
        return self.source_node

    def set_target_node(self, new_target_node):
        self.target_node = new_target_node

    def get_target_node(self):
        return self.target_node


class SubArc(Arc):
    """subArc class: subgraph"""

    def __init__(self, source_node, target_node):
        self.ident = source_node.get_ident() + '->' + target_node.get_ident()
        self.source_node = source_node
        self.target_node = target_node

    def get_class(self):
        print('SubArc class')


class Node:

    def __init__(self, ident):
        self.ident = ident
        self.list_activities = []
        self.succ_nodes = []
        self.subgraphs = {}

    def add_activity(self, activity):
        self.list_activities.append(activity)

    # def add_activities(self, *activities):
    #     self.list_activities.extend(activities)

    def remove_activity(self, Activity):
        self.list_activities.remove(Activity)

    def add_activities(self, Activities):
        self.list_activities.extend(Activities)

    def get_list_activities(self):
        return self.list_activities

    def add_subgraph(self, subgraph):
        self.subgraphs.setdefault(
            subgraph.get_ident(), []).append(subgraph.get_nodes())
        self.subgraphs.setdefault(
            subgraph.get_ident(), []).append(subgraph.get_arcs())

    def add_node_subgraph(self, node, subgraph_ident):
        # self.subgraphs[subgraph_ident][0].append(node)
        self.subgraphs[subgraph_ident][0].append(node)

    def add_arc_subgraph(self, arc, subgraph_ident):
        self.subgraphs[subgraph_ident][1].append(arc)

    def find_activity(self, Activity):
        if Activity in self.list_activities:
            return True
        else:
            return False

    def get_subgraphs(self):
        return self.subgraphs

    def get_ident(self):
        return self.ident

    def set_ident(self, new_ident):
        self.ident = new_ident

    def calcule_max_time(self):
        max_time = 0
        if self.list_activities:
            #print([value for value in self.list_activites])
            max_time = max(activ.get_max_execu_time()
                           for activ in self.list_activities)
        if self.subgraphs:
            for subgraph in self.subgraphs:
                # self.subgraphs[subgraph][0][0])
                temps_max_time = SubGraph(
                    'a', self.subgraphs[subgraph][0], self.subgraphs[subgraph][1]).calcule_max_time()
                max_time = max(max_time, temps_max_time)
        return max_time

    def calcule_min_time(self):
        min_time = 0  # float('inf')
        if self.list_activities:
            min_time = max(activ.get_min_execu_time()
                           for activ in self.list_activities)
        if self.subgraphs:
            # print(self.subgraphs)
            for subgraph in self.subgraphs:
                # (self.subgraphs[subgraph][0][0])
                temps_min_time = SubGraph(
                    'a', self.subgraphs[subgraph][0], self.subgraphs[subgraph][1]).calcule_min_time()
                min_time = max(min_time, temps_min_time)
        return min_time


class SubNode(Node):

    def __init__(self, ident):
        self.ident = ident
        self.list_activites = []
        self.succ_nodes = []
        self.subgraphs = {}

    def get_ident(self):
        return self

    def get_class(self):
        print('SubNode')


class NullNode(SubNode):
    def __init__(self, ident):
        self.ident = ident
        self.list_activites = []
        self.succ_nodes = []
        self.subgraphs = {}

    def get_ident(self):
        return self.get_ident()

    def get_class(self):
        print('NullNode')
