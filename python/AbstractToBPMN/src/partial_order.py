#/usr/bin/env python3
# -*- coding:utf-8 -*-
# author: ahzm
# update: Sept 30, 2021

"""
Partial order Module: PratialOrder class
"""

from basic_class import *
from abstract_graph import *
import networkx as nx

class PartialOrder:

    def __init__(self, list_activities, couples_activities):
        self.list_activities    = list_activities
        # self.couples_activities = couples_activities
        self.couples_activities = self.filter_couples_activities(couples_activities)
        self.nodes = []
        self.arcs  = []
        self.succ_dict = self.generate_succ_dict() # succ activities dict
        self.precu_dict = self.generate_precu_dict() # precu activities dict
        self.dict_succ_graph = self.generate_dict_succ_graph() #nodes

    def filter_couples_activities(self, couples_activities):
        
        filter_couples = []

        graph = nx.DiGraph()
        for activ in self.list_activities:
            graph.add_node(activ)
        
        for couple_activ in couples_activities:
            graph.add_edge(couple_activ[0], couple_activ[1])
        
        min_graph = nx.transitive_reduction(graph)

        for edge in min_graph.edges:
            filter_couples.append([edge[0], edge[1]])

        return filter_couples

    def generate_dict_succ_graph(self):
        succ_graph = {}
        for node in self.nodes:
            succ_graph.setdefault(node,[])
            for arc in self.arcs:
                if (node == arc.get_source_node()):
                    succ_graph.setdefault(node,[]).append(arc.get_target_node())
        return succ_graph

    def add_activity(self, Activity):
        self.list_activities.append(Activity)

    def add_partial_order(self, couple_activities):
        self.couples_activities.append(couple_activities)

    def generate_succ_dict(self):
        succ_dict = {}
        for activity in self.list_activities:
            succ_dict.setdefault(activity, [])
        for couple_activities in self.couples_activities:
            if couple_activities[1] not in succ_dict[couple_activities[0]]:
                succ_dict[couple_activities[0]].append(couple_activities[1])
        return succ_dict

    def generate_precu_dict(self):
        precu_dict ={}
        for activity in self.list_activities:
            precu_dict.setdefault(activity, [])
        for couple_activities in self.couples_activities:
            precu_dict[couple_activities[1]].append(couple_activities[0])
        return precu_dict

    def find_activity_nodes(self, activity, subnodes=None):
        
        if subnodes:
            nodes = subnodes[:]
        else:
            nodes = self.nodes
        
        for node in nodes:
            #print('act :', activity.get_ident(), activity)
            #print('list:', [activ.get_ident() for activ in node.get_list_activities()])
            if activity in node.get_list_activities():
                # print(activity.get_ident(), activity)
                # print(node)
                return node
        #for node in nodes:
            if node.get_subgraphs():
                # print('len', node.get_subgraphs())
                # print('subgraph_1' in node.get_subgraphs())
                # if 'subgraph_1' in node.get_subgraphs():
                #     print(node.get_subgraphs()['subgraph_1'][0])
                #print( 'hhh', node.get_subgraphs()['subgraph_1'])
                for subgraph_key in node.get_subgraphs().keys():
                    #print(subgraph_key)
                    subgraph_nodes = node.get_subgraphs()[subgraph_key][0]
                    # print(node.get_subgraphs()[subgraph_key][0])
                    # for node in subgraph_nodes:
                    #     if activity in node.get_list_activities():
                    #         return node
                    # print('subgraph--------------- :', subgraph_nodes)
                    return self.find_activity_nodes(activity, subgraph_nodes)
        return False
    
    def check_other_actvis_node(self, activity, node):
        if len(node.get_list_activities()) >= 2:
            return True
        if len(node.get_subgraphs()) >=1 :
            return True
        return False

    def find_node(self, node_find):
        
        #node_find = node_find
        #nodes = self.nodes

        if node_find in self.nodes:
            return node_find, False
        
        for node in self.nodes:
            if node.get_subgraphs():
                for subgraph_key in node.get_subgraphs():
                    #return self.find_node(node_find, node.get_subgraphs()[subgraph_key][0])
                    if node_find in node.get_subgraphs()[subgraph_key][0]:
                        return node, subgraph_key
        return False

    def check_arc_nodes(self, source_node, target_node):
        for arc in self.arcs:
            if arc.get_source_node() == source_node and arc.get_target_node() == target_node:
                return arc
        return False
    
    def check_all_activities(self):
        list_activ_unassigns = []
        for activ in self.list_activities:
            if self.succ_dict[activ] == [] and self.precu_dict[activ] == []:
                list_activ_unassigns.append(activ)
        if list_activ_unassigns:
            return list_activ_unassigns
        else: 
            return False

    def change_self_nodes_arcs(self):
        if self.check_all_activities():
            node_final = Node('node_final')
            node_final.add_activities(self.check_all_activities())
            subgraph_final = SubGraph('subgraph_final', self.nodes, self.arcs)
            node_final.add_subgraph(subgraph_final)
            self.nodes = [node_final]
            self.arcs  = []

    def check_partiel_order(self):
        for precu_key in self.precu_dict.keys():
            if len(self.precu_dict[precu_key]) > 1:
                print("False")
                return False
        return True

    def modify_all_idents(self):
        for node in self.nodes:
            new_name = 'node'
            for avtiv in node.get_list_activities():
                new_name = new_name + '_' + avtiv.get_ident()
            if len(node.get_list_activities()) == 0:
                new_name = new_name + '_0'
            new_name = new_name + '_' + str(len(node.get_subgraphs()))
            node.set_ident(new_name)
            #print(node.get_ident(), [activ.get_ident() for activ in node.get_list_activities()])

        for arc in self.arcs:
            new_name_arc = arc.get_source_node().get_ident() + '->' + arc.get_target_node().get_ident()
            arc.set_ident(new_name_arc)


    def findPath(self, graph,start,end,path=[]):   
        path = path + [start]
        if start == end:
            return path 
        for node in graph[start]:
            if node not in path:
                newpath = findPath(graph,node,end,path)
                if newpath:
                    return newpath
        return None

    def findAllPath(self, graph,start,end,path=[]):
        # path = []
        path = path + [start]
        #path.append(start)
        if start == end:
            return [path]

        paths = []  
        for node in graph[start]:
            if node not in path:
                newpaths = self.findAllPath(graph,node,end,path) 
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    def getAllPaths(self):
        list_starts = []
        list_ends = []

        #flag_len_succ_activs = True
        for key_activ, values_actives in self.succ_dict.items():
            # if len(values_actives) > 1:
            #     flag_len_succ_activs = False
            if len(values_actives) == 0:
                list_ends.append(key_activ)

        for key_activ, values_actives in self.precu_dict.items():
            # if len(values_actives) > 1:
            #     flag_len_succ_activs = False
            if len(values_actives) == 0:
                list_starts.append(key_activ)
        # print("***************************")
        # print("list_starts:", list_starts)
        # print("list_ends:", list_ends)
        # print("***************************")
        paths = []
        for start in list_starts:
            for end in list_ends:
                paths.extend(self.findAllPath(self.succ_dict, start, end, path=[]))
        # print("All Paths(", len(paths), "):")
        # for path in paths:
        #     print([act.get_ident() for act in path])
        # print("***************************")
        return paths

    def split_paths(self, paths):

        list_nodes = []
        list_arcs = []
        for path in paths[:]:
            if len(path) == 0:
                #print("1. paths:", path)
                paths.remove(path)
        # if len(paths) == 0:
        #     return list_nodes, list_arcs      

        if len(paths) == 1:
            for activ in paths[0]:
                activ_node = Node("node_" + activ.get_ident())
                activ_node.add_activity(activ)
                list_nodes.append(activ_node)
            for i in range(len(list_nodes)):
                if i + 1 < len(list_nodes):
                    list_arcs.append(Arc(list_nodes[i], list_nodes[i+1]))
            return list_nodes, list_arcs
        
        if len(paths) >= 2:
            #print("paths:", paths)
            dict_div_activs = {}
            count = 0
            list_inter_paths = list(set(paths[0]).intersection(*paths[1:]))
            list_inter_paths.sort(key=paths[0].index)
            #print("list_inter_paths:",len(list_inter_paths), [act.get_ident() for act in list_inter_paths], list_inter_paths)

            if len(list_inter_paths) == 0:
                #print("list_inter_paths == 0")
                one_node = Node("node_one_node")
                count_sg = 1
                new_paths = []
                for path in paths:
                    #print("paths:", paths)
                    if len(path) == 1:
                        #print("path[0]:", path[0].get_ident())
                        one_node.add_activity(path[0])
                    #elif len(path) > 2:
                    else:
                        new_paths.append(path)
                if len(paths) != len(new_paths):
                    #print("paths is not equal new_paths")
                    #print("new_paths:", new_paths)
                    if len(new_paths) >=1:
                        #print("New Paths:")
                        # for path in new_paths:
                        #     print([act.get_ident() for act in path])
                        temp_nodes, temp_arcs = self.split_paths(new_paths)
                        temp_subgraph = SubGraph('subgraph_'+ str(count_sg), temp_nodes , temp_arcs)
                        one_node.add_subgraph(temp_subgraph)
                        count_sg += 1
                        # new_list_inter_paths = list(set(new_paths[0]).intersection(*new_paths[1:]))
                        # new_list_inter_paths.sort(key=new_paths[0].index)
                        # print("new_list_inter_paths:", [act.get_ident() for act in new_list_inter_paths])
                        # if new_list_inter_paths: 
                        #     print("new list inter paths > 0")
                        #     temp_nodes, temp_arcs = self.split_paths(new_paths)
                        #     temp_subgraph = SubGraph('subgraph_'+ str(count_sg), temp_nodes , temp_arcs)
                        #     one_node.add_subgraph(temp_subgraph)
                        #     count_sg += 1
                        # else:
                        #     #print("error ")
                        #     for new_path in new_paths:
                        #         temp_nodes, temp_arcs = self.split_paths([new_path])
                        #         temp_subgraph = SubGraph('subgraph_'+ str(count_sg), temp_nodes , temp_arcs)
                        #         one_node.add_subgraph(temp_subgraph)
                        #         count_sg += 1
                else:
                    for path in paths:
                        temp_nodes, temp_arcs = self.split_paths([path])
                        temp_subgraph = SubGraph('subgraph_'+ str(count_sg), temp_nodes , temp_arcs)
                        one_node.add_subgraph(temp_subgraph)
                        count_sg += 1
                list_nodes.append(one_node)
                return list_nodes, list_arcs


                # for path in paths:
                #     if len(path) == 1:
                #         one_node.add_activity(path[0])
                #     else:
                #         temp_nodes, temp_arcs = self.split_paths([path])
                #         temp_subgraph = SubGraph('subgraph_'+ str(count_sg), temp_nodes , temp_arcs)
                #         one_node.add_subgraph(temp_subgraph)
                #         count_sg += 1
                # list_nodes.append(one_node)
                # return list_nodes, list_arcs

            if len(list_inter_paths) == 1:
                if list_inter_paths[0] == paths[0][0]:
                    first_node = Node("node_" + list_inter_paths[0].get_ident())
                    first_node.add_activity(list_inter_paths[0])
                    new_paths = []

                    # flag = True
                    # length = len(paths[0])
                    for path in paths:
                        if len(path)>1: 
                            new_paths.append(path[1:])
                        if len(path) == 1:
                            #if [path[0]] not in new_paths:
                            new_paths.append([path[0]])
                        # if length != len(path):
                        #     flag = False
                    #print("****new_paths:" , new_paths)
                    # if flag:
                    #     list_nodes.append(first_node)
                    #     return list_nodes, list_arcs

                    #if new_paths:
                    #temp_nodes, temp_arcs = self.split_paths(new_list_inter_paths)
                    temp_nodes, temp_arcs = self.split_paths(new_paths)
                    list_nodes.append(first_node)
                    list_nodes.extend(temp_nodes)
                    list_arcs.append(Arc(first_node, temp_nodes[0]))
                    return list_nodes, list_arcs
                    # else:
                    #     list_nodes.append(first_node)
                    #     return list_nodes, list_arcs

                elif list_inter_paths[0] == paths[0][-1]:
                    last_node = Node("node_" + list_inter_paths[0].get_ident())
                    last_node.add_activity(list_inter_paths[0])
                    new_paths = []
                    for path in paths:
                        new_paths.append(path[:-1])
                    #print("new_paths:" , new_paths)
                    temp_nodes, temp_arcs = self.split_paths(new_paths)
                    list_nodes.extend(temp_nodes)
                    list_nodes.append(last_node)
                    list_arcs.append(Arc(temp_nodes[0], last_node))
                    return list_nodes, list_arcs
                else:
                    temp_path1 = []
                    temp_path2 = []

                    for path in paths:
                        temp_index = path.index(list_inter_paths[0])
                        #print("temp_index", temp_index)
                        temp_path1.append(path[:temp_index])
                        temp_path2.append(path[temp_index+1:])

                    #print("temp_paths1:", temp_path1)
                    #print("temp_paths2:",temp_path2)

                    new_temp_paths1 =  [list(t) for t in set(tuple(_) for _ in temp_path1)]
                    new_temp_paths2 =  [list(t) for t in set(tuple(_) for _ in temp_path2)]

                    #print("new_temp_paths1:", new_temp_paths1)
                    #print("new_temp_paths2:",new_temp_paths2)

                    temp_nodes_1, temp_arcs_1 = self.split_paths(new_temp_paths1)
                    temp_nodes_2, temp_arcs_2 = self.split_paths(new_temp_paths2)
                    mid_node = Node('node_'+ list_inter_paths[0].get_ident())
                    mid_node.add_activity(list_inter_paths[0])
                    list_nodes.extend(temp_nodes_1)
                    list_nodes.append(mid_node)
                    list_nodes.extend(temp_nodes_2)
                    list_arcs.append(Arc(temp_nodes_1[0], mid_node))
                    list_arcs.append(Arc(mid_node, temp_nodes_2[0]))
                    return list_nodes, list_arcs

            if len(list_inter_paths) >= 2:
                first_flag = False
                last_flag = False
                if list_inter_paths[0] == paths[0][0]:
                    #print("yes_start_node")
                    first_flag = True
                    first_node = Node("node_" + list_inter_paths[0].get_ident())
                    #print(list_inter_paths[0].get_ident())
                    first_node.add_activity(list_inter_paths[0])
                if list_inter_paths[-1] == paths[0][-1]:
                    #print("yes_end_node")
                    last_flag = True
                    last_node = Node("node_" + list_inter_paths[-1].get_ident())
                    last_node.add_activity(list_inter_paths[-1])
                

                if first_flag and last_flag:
                    len_shared = len(list_inter_paths[1:-1])
                    #print(list_inter_paths[1:-1])
                    
                    new_paths = []
                    for path in paths:
                        new_paths.append(path[1:-1])

                    if len_shared == 0:
                        temp_nodes, temp_arcs = self.split_paths(new_paths)
                        list_nodes.append(first_node)
                        list_nodes.extend(temp_nodes)
                        list_nodes.append(last_node)
                        list_arcs.append(Arc(first_node, temp_nodes[0]))
                        list_arcs.append(Arc(temp_nodes[0], last_node))
                        return list_nodes, list_arcs
                    else:
                        temp = 0
                        list_nodes.append(first_node)
                        for shared_ele in list_inter_paths[1:-1]:
                            new_temp_paths = []
                            
                            for path in new_paths:
                                temp_index = path.index(shared_ele)
                                new_temp_paths.append(path[temp:temp_index])
                            temp = temp_index + 1

                            if len(new_temp_paths):
                                temp_nodes, temp_arcs = self.split_paths(new_temp_paths)
                                mid_node = Node('node_' + shared_ele.get_ident())
                                mid_node.add_activity(shared_ele)
                                list_nodes.extend(temp_nodes)
                                list_nodes.append(mid_node)
                        list_nodes.append(last_node)
                        for i in range(len(list_nodes)):
                            if i + 1 < len(list_nodes):
                                list_arcs.append(Arc(list_nodes[i], list_nodes[i+1]))
                        return list_nodes, list_arcs

                elif first_flag == True and last_flag == False:
                    len_shared = len(list_inter_paths[1:])
                    #print("last", list_inter_paths[1:])
                    #print([act.get_ident() for act in  list_inter_paths[1:]])
                    new_paths = []
                    for path in paths:
                        new_paths.append(path[1:])
                    

                    #print("new_paths:", new_paths)
                    if len_shared == 0:
                        #print("len shared == 0")
                        temp_nodes, temp_arcs = self.split_paths(new_paths)
                        list_nodes.append(first_node)
                        list_nodes.extend(temp_nodes)
                        list_arcs.append(Arc(first_node, temp_nodes[0]))
                        return list_nodes, list_arcs
                    else:
                        #print("len shared != 0")
                        temp = 0
                        list_nodes.append(first_node)
                        for shared_ele in list_inter_paths[1:]:
                            new_temp_paths = []
                            for path in new_paths:
                                temp_index = path.index(shared_ele)
                                #print("path:", [act.get_ident() for act in path])
                                #print("temp_index:", temp_index)
                                # if temp_index == 0:
                                #     #if [path[0]] not in new_temp_paths:
                                #     #new_temp_paths.append([path[0]])
                                #     pass
                                # else:
                                    #if path[temp:temp_index] not in new_temp_paths:
                                new_temp_paths.append(path[temp:temp_index])
                            temp = temp_index + 1
                            # print("temp_index:", temp_index)
                            # if len(new_temp_paths) >= 1:
                            #print("length of new_temp_paths:", len(new_temp_paths), new_temp_paths)
                            if len(new_temp_paths[0]) != 0:
                                temp_nodes, temp_arcs = self.split_paths(new_temp_paths)
                                list_nodes.extend(temp_nodes)
                            mid_node = Node('node_' + shared_ele.get_ident())
                            mid_node.add_activity(shared_ele)
                                
                            list_nodes.append(mid_node)

                        new_temp_paths= []
                        for path in new_paths:
                            #if path[temp:] not in new_temp_paths1:
                            new_temp_paths.append(path[temp:])

                        if len(new_temp_paths):
                            #print("length of new_temp_paths:", len(new_temp_paths), new_temp_paths)
                            temp_nodes, temp_arcs = self.split_paths(new_temp_paths)
                            # mid_node = Node('node_' + shared_ele.get_ident())
                            # mid_node.add_activity(shared_ele)
                            list_nodes.extend(temp_nodes)
                            #list_nodes.append(mid_node)

                        for i in range(len(list_nodes)):
                            if i + 1 < len(list_nodes):
                                list_arcs.append(Arc(list_nodes[i], list_nodes[i+1]))
                        return list_nodes, list_arcs
                    

                elif first_flag == False and last_flag == True:
                    len_shared = len(list_inter_paths[:-1])
                    #print(list_inter_paths[:-1])
                    new_paths = []
                    for path in paths:
                        new_paths.append(path[:-1])
                    
                    if len_shared == 0:
                        temp_nodes, temp_arcs = self.split_paths(new_paths)
                        list_nodes.extend(temp_nodes)
                        list_nodes.append(last_node)
                        list_arcs.append(Arc(temp_nodes[0], last_node))
                        return list_nodes, list_arcs
                    else:
                        temp = 0
                        for shared_ele in list_inter_paths[:-1]:
                            new_temp_paths = []
                            
                            for path in new_paths:
                                temp_index = path.index(shared_ele)
                                new_temp_paths.append(path[temp:temp_index])
                            temp = temp_index + 1

                            if len(new_temp_paths):
                                temp_nodes, temp_arcs = self.split_paths(new_temp_paths)
                                mid_node = Node('node_' + shared_ele.get_ident())
                                mid_node.add_activity(shared_ele)
                                list_nodes.extend(temp_nodes)
                                list_nodes.append(mid_node)
                        list_nodes.append(last_node)
                        for i in range(len(list_nodes)):
                            if i + 1 < len(list_nodes):
                                list_arcs.append(Arc(list_nodes[i], list_nodes[i+1]))
                        return list_nodes, list_arcs

                elif first_flag == False and last_flag == False:
                    
                    new_paths = paths[:]
                    temp = 0
                    for shared_ele in list_inter_paths[:]:
                        new_temp_paths = []
                        
                        for path in new_paths:
                            temp_index = path.index(shared_ele)
                            new_temp_paths.append(path[temp:temp_index])
                        temp = temp_index + 1

                        if len(new_temp_paths):
                            temp_nodes, temp_arcs = self.split_paths(new_temp_paths)
                            mid_node = Node('node_' + shared_ele.get_ident())
                            mid_node.add_activity(shared_ele)
                            list_nodes.extend(temp_nodes)
                            list_nodes.append(mid_node)
                    for i in range(len(list_nodes)):
                        if i + 1 < len(list_nodes):
                            list_arcs.append(Arc(list_nodes[i], list_nodes[i+1]))
                    return list_nodes, list_arcs

    def generate_abstract_model(self):


        paths = self.getAllPaths()
        list_nodes, list_arcs = self.split_paths(paths)
        self.nodes = list_nodes[:]
        self.arcs = list_arcs[:]

        # for key_activ, values_activs in self.succ_dict.items():
            
        #     key_node = self.find_activity_nodes(key_activ)
        #     if not key_node and values_activs:
        #         new_key_node = Node('node_' + key_activ.get_ident())
        #         #print('cree_key_node,' , new_key_node.get_ident())
        #         self.nodes.append(new_key_node)
        #         new_key_node.add_activity(key_activ)

        #     if values_activs:
        #         unassigned_activities = []
        #         key_node =  self.find_activity_nodes(key_activ)
        #         # print('key_node,' , key_node)
        #         # print(key_activ.get_ident(), 'find_node, ', self.find_node(key_node))
        #         node_key_node, subgraph_key_node = self.find_node(key_node)
        #         check_other_activs = self.check_other_actvis_node(key_activ, key_node) #check if other activ in same node
        #         for activ in values_activs:
        #             activ_node = self.find_activity_nodes(activ)
        #             #print('node : ', activ_node)
        #             # if activ_node:
        #             #    node_activ_node, subgraph_activ_node =  self.find_node(activ_node)
        #             if not activ_node:
        #                 unassigned_activities.append(activ)

        #         if len(unassigned_activities) == len(values_activs):
        #             #print('********', key_activ.get_ident(), '__', [value.get_ident() for value in unassigned_activities])
        #             new_node = Node('init_succ_node_' + key_activ.get_ident())
        #             new_node.add_activities(unassigned_activities)
        #             # print('new_node', [acti for acti in new_node.get_list_activities()])
        #             # print('new_node', new_node)
        #             # print('check', check_other_activs)
        #             if not check_other_activs:
        #                 if not subgraph_key_node:
        #                     self.nodes.append(new_node)
        #                     tmp_arc = self.check_arc_nodes(key_node, new_node)
        #                     if not tmp_arc:
        #                         self.arcs.append(Arc(key_node, new_node))
        #                 else:
        #                     node_key_node.add_node_subgraph(new_node, subgraph_key_node)
        #                     node_key_node.add_arc_subgraph(Arc(key_node, new_node), subgraph_key_node)
        #             elif check_other_activs:
        #                 key_node.remove_activity(key_activ)
        #                 new_key_node = Node('node_' + key_activ.get_ident())
        #                 new_key_node.add_activity(key_activ)
        #                 compte_subgraphs = len(key_node.get_subgraphs())
        #                 subgraphs_nodes = [new_key_node, new_node]
        #                 subgraphs_arcs = [Arc(new_key_node, new_node)]
        #                 new_subgraph = SubGraph('subgraph_' + str(compte_subgraphs), subgraphs_nodes, subgraphs_arcs)
        #                 #print('----------', new_subgraph.get_nodes())
        #                 #print('----------', [node.get_list_activities() for node in new_subgraph.get_nodes()])
        #                 key_node.add_subgraph(new_subgraph)
        #         else:
        #             multip_precu = [val for val in values_activs if val not in unassigned_activities]
        #             #print([a.get_ident() for a in multip_precu])
        #             raise Exception('Activity :{} has multiple precursor activities'.format(multip_precu[0].get_ident()))
        #self.change_self_nodes_arcs()
        self.modify_all_idents()
        return self.nodes, self.arcs


# if __name__ == "__main__":

#     act1 = Activity(1,2,1,1)
#     act2 = Activity(2,3,1,1)
#     act3 = Activity(3,3,1,1)
#     act4 = Activity(4,3,1,1)
#     act5 = Activity(5,3,1,1)
#     act6 = Activity(6,2,1,1)
#     act7 = Activity(7,3,1,1)
#     act8 = Activity(8,3,1,1)
#     act9 = Activity(9,3,1,1)
#     act10 = Activity(10,3,1,1)
#     #list_activs = [act1, act2, act3, act4, act5, act6, act7, act8, act9, act10]
#     #list_activs = [act4, act5, act6, act7, act8, act9, act10]
#     #list_op = [[act1, act4], [act2, act4], [act3, act4], [act4, act5], [act4, act6], [act5, act7], [act5, act8], [act8, act9], [act8, act10]]
#     #list_op = [[act4, act5], [act4, act6], [act5, act7], [act5, act8], [act8, act9], [act8, act10]]
   
#     list_activs = [act1, act2, act3, act4, act5, act6]
#     list_op = [[act1, act2], [act1, act3], [act3, act4], [act4, act5], [act4, act6]] 

#     list_activs = [act1, act2, act3]
#     list_op = [[act1, act2], [act1, act3]] 
#     po = PartialOrder(list_activs, list_op)
#     nodes, arcs = po.generate_abstract_model()

#     print("nodes, arcs:", [node.get_list_activities() for node in nodes], arcs)
#     print([node.get_ident() for node in nodes], arcs)
#     print(nodes[-1].get_subgraphs())
#     for subgraph in nodes[-1].get_subgraphs():
#        print("sub:", [node.get_list_activities() for node in nodes[-1].get_subgraphs()[subgraph][0]])


#     from bpmn_class import *
#     BPMNGraph = AbsToBPMNGraph(nodes, arcs)
#     new_nodes, new_arcs = BPMNGraph.get_BPMN_graph()
#     print('------------BPMN---------------')
#     print('BPMN nodes:', len(new_nodes))
#     print([node.get_ident() for node in new_nodes])
#     print('BPMN arcs:', len(new_arcs))
#     print([arc.get_ident() for arc in new_arcs])
#     print('-------------------------------')


