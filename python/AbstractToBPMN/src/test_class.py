# /usr/bin/env python3
# -*- coding:utf-8 -*-
# author: Ahang
# update: Jan 05, 2021

"""
Test Module:
1) TestPartialOrder
2) TestBPMN
3) AutoTest : Table in article
"""

import time
import random

from basic_class import *
from partial_order import *
from abstract_graph import *
from bpmn_class import *
from py2pif import *

# Decorator is used to calculate function execution time


def display_time(func):
    def wrapper(*args):
        t1 = time.time()
        func(*args)
        t2 = time.time()
        print('ExcTime:', t2 - t1)
    return wrapper


class AutoTest:

    def get_nodes_arcs(self, n, m):
        nodes = []
        arcs = []
        for i in range(m):
            node_i = Node(str(i))
            nodes.append(node_i)
            for j in range(int(n/m)):
                node_i.add_activity(Activity(str(j), 1, 2))
        # print(n%m)
        for i in range(n % m):
            nodes[i].add_activity(Activity(str(i), 1, 2))
        # print(len(nodes[0].get_list_activities()))
        if m == 5:
            arcs = [Arc(nodes[0], nodes[1]), Arc(nodes[0], nodes[2]),
                    Arc(nodes[2], nodes[3]), Arc(nodes[3], nodes[4])]
        else:
            #new_arcs = []
            count = 0
            # random.seed(10)
            for i in range(1, m):
                if m < 100:
                    if count % 5 != 0 or count == 0:
                        arcs.append(Arc(nodes[count], nodes[i]))
                    if count % 5 == 0 and count != 0:
                        temp = count
                        ram_temp = random.randint(2, 5)
                        for j in range(1, ram_temp):
                            arcs.append(Arc(nodes[temp - j], nodes[temp+1]))
                            temp += 1
                else:
                    if count % (int(m*0.07)) != 0 or count == 0:
                        arcs.append(Arc(nodes[count], nodes[i]))
                    if count % (int(m*0.07)) == 0 and count != 0:
                        temp = count
                        ram_temp = random.randint(2, 5)
                        for j in range(1, ram_temp):
                            arcs.append(Arc(nodes[temp - j], nodes[temp+1]))
                            #temp += 1
                count += 1
                #print('len',len(new_arcs), [arc.get_ident() for arc in new_arcs])
        return nodes, arcs

    @display_time
    def test_task_nodes(self, n, m, type_=0):
        print('------------start-----------')
        nodes, arcs = self.get_nodes_arcs(n, m)
        if type_ == 0:
            print('node:', len(nodes))
            print('arc:', len(arcs))
            start = time.time()
            abgraph = AbstractGraph(nodes, arcs)
            abgraph.calcule_min_time()
            # abgraph.calcule_max_time()
            end = time.time()
            print('time', str(end - start))
        else:
            start = time.time()
            bpmn_model = AbsToBPMNGraph(nodes, arcs)
            bpmn_nodes, bpmn_arcs = bpmn_model.get_BPMN_graph()
            end = time.time()
            print('time', str(end - start))
            print('node:', len(bpmn_nodes))
            print('arc:', len(bpmn_arcs))
            count_p = 0
            count_e = 0
            for node in bpmn_nodes:
                if isinstance(node, ParalNode):
                    count_p += 1
                if isinstance(node, ExcluNode):
                    count_e += 1
            print('Para:', count_p)
            print('Exclu:', count_e)

        print('------------end-----------')

    def test_cases(self):
        test_cases = [[10, 5], [50, 30], [100, 30], [100, 50],
                      [500, 100], [500, 300], [1000, 500], [10000, 1000]]
        for case in test_cases:
            for ty in [0, 1]:
                self.test_task_nodes(case[0], case[1], ty)


class TestPartialOrder:

    @display_time
    def test_partial_order(self):
        act1 = Activity('1', 1, 2)
        act2 = Activity('2', 1, 5)
        act3 = Activity('3', 7, 14)
        act4 = Activity('4', 1, 2)
        act5 = Activity('5', 1, 2)
        act6 = Activity('6', 1, 2)
        act7 = Activity('7', 1, 3)
        act8 = Activity('8', 1, 2)
        act9 = Activity('9', 3, 10)
        act10 = Activity('10', 3, 5)

        list_activities = [act1, act2, act3, act4,
                           act5, act6, act7, act8, act9, act10]
        list_ordrepartiel = [[act1, act2], [act2, act3], [act3, act4], [act4, act5], [
            act4, act6], [act5, act7], [act5, act8], [act5, act10], [act8, act9]]
        op_test = PartialOrder(list_activities, list_ordrepartiel)
        abs_nodes, abs_arcs = op_test.generate_abstract_model()

        #print("list_nodes_activs", len(abs_nodes), [node.get_list_activities() for node in abs_nodes])
        #print("list_nodes_subgraph", len(abs_nodes), [node.get_subgraphs() for node in abs_nodes])
        print("list_nodes", len(abs_nodes), [node for node in abs_nodes])
        print("list_arcs", len(abs_arcs), [arc for arc in abs_arcs])

        abstractGraph = AbstractGraph(abs_nodes, abs_arcs)
        print(abstractGraph.get_min_time())
        print(abstractGraph.get_max_time())
        BPMNGraph = AbsToBPMNGraph(abs_nodes, abs_arcs)
        new_nodes, new_arcs = BPMNGraph.get_BPMN_graph()
        print('------------BPMN---------------')
        print('BPMN nodes:', len(new_nodes))
        print([node.get_ident() for node in new_nodes])
        print('BPMN arcs:', len(new_arcs))
        print([arc.get_ident() for arc in new_arcs])
        print('-------------------------------')


class TestBPMN:

    @display_time
    def test_bpmn(self):
        act1 = Activity('a', 1, 2)
        act2 = Activity('b', 2, 4)
        act3 = Activity('c', 2, 5)
        act4 = Activity('d', 1, 10)
        act5 = Activity('e', 10, 2000)
        act6 = Activity('f', 10, 2000)

        node_a = Node('node_a')
        node_b = Node('node_b')

        node_a.add_activity(act1)
        node_a.add_activity(act5)
        node_b.add_activity(act4)

        node_c = Node('node_c')
        node_d = Node('node_d')
        node_e = Node('node_e')
        node_c.add_activity(act2)
        node_c.add_activity(act6)
        node_d.add_activity(act3)
        node_e.add_activity(act5)
        subnodes = [node_c, node_d, node_e]
        subarcs = [Arc(node_c, node_d), Arc(node_c, node_e)]
        node_b.add_subgraph(SubGraph('Gs', subnodes, subarcs))
        nodes = [node_a, node_b]
        arcs = [Arc(node_a, node_b)]
        abgraph = AbstractGraph(nodes, arcs)

        print('start_node:', abgraph.get_start_node().get_ident())
        print('end_node:', [end_node.get_ident()
              for end_node in abgraph.get_end_node()])
        print('----------------')
        print('Execution time:')
        print("(1) min_time:", abgraph.calcule_min_time())
        print("(2) max_time:", abgraph.calcule_max_time())
        print('----------------')
        BPMNModel = AbsToBPMNGraph(nodes, arcs)
        new_nodes, new_arcs = BPMNModel.transfor_all_nodes()
        print('------------BPMN---------------')
        print('BPMN nodes:', len(new_nodes))
        print(hex(id(new_nodes[3])))
        print(new_nodes)
        print([node.get_ident() for node in new_nodes])
        print('BPMN arcs:', len(new_arcs))
        print([arc.get_ident() for arc in new_arcs])
        print('-------------------------------')

    def test_compute(self):
        act1 = Activity('a', 1, 1)
        act2 = Activity('b', 2, 2)
        act3 = Activity('c', 3, 3)
        act4 = Activity('d', 4, 4)

        node_a = Node("a")
        node_b = Node("b")
        node_c = Node("c")

        node_a.add_activity(act1)
        node_b.add_activity(act2)
        node_b.add_activity(act3)
        node_c.add_activity(act4)

        nodes = [node_a, node_b, node_c]
        arcs = [Arc(node_a, node_b), Arc(node_b, node_c)]

        abgraph = AbstractGraph(nodes, arcs)
        print('Execution time:')
        print("(1) min_time:", abgraph.calcule_min_time())
        print("(2) max_time:", abgraph.calcule_max_time())
        print('----------------')

    def test_pif(self):
        act1 = Activity('a', 1, 2)
        act2 = Activity('b', 2, 4)
        act3 = Activity('c', 2, 5)
        act4 = Activity('d', 1, 10)
        act5 = Activity('e', 10, 2000)
        act6 = Activity('f', 10, 2000)
        act7 = Activity('g', 10, 2000)

        node_a = Node('node_a')
        node_b = Node('node_b')

        node_a.add_activity(act1)
        node_a.add_activity(act5)
        node_b.add_activity(act4)

        node_c = Node('node_c')
        node_d = Node('node_d')
        node_e = Node('node_e')
        node_c.add_activity(act2)
        node_c.add_activity(act6)
        node_d.add_activity(act3)
        node_e.add_activity(act7)
        subnodes = [node_c, node_d, node_e]
        subarcs = [Arc(node_c, node_d), Arc(node_c, node_e)]
        node_b.add_subgraph(SubGraph('Gs', subnodes, subarcs))
        nodes = [node_a, node_b]
        arcs = [Arc(node_a, node_b)]
        abgraph = AbstractGraph(nodes, arcs)

        print('start_node:', abgraph.get_start_node().get_ident())
        print('end_node:', [end_node.get_ident()
              for end_node in abgraph.get_end_node()])
        print('----------------')
        print('Execution time:')
        print("(1) min_time:", abgraph.calcule_min_time())
        print("(2) max_time:", abgraph.calcule_max_time())
        print('----------------')
        BPMNModel = AbsToBPMNGraph(nodes, arcs)
        new_nodes, new_arcs = BPMNModel.transfor_all_nodes()
        print('------------BPMN---------------')
        print('BPMN nodes:', len(new_nodes))
        # print(hex(id(new_nodes[3])))
        print(new_nodes)
        print([node.get_ident() for node in new_nodes])
        print('BPMN arcs:', len(new_arcs))
        print([arc.get_ident() for arc in new_arcs])
        print('-------------------------------')

        pytopif = Py2Pif("new")
        pytopif.getPIFXML(new_nodes, new_arcs)

    def test_pif_simple(self):
        act1 = Activity('a', 1, 2)
        node_a = Node('node_a')
        node_a.add_activity(act1)
        nodes = [node_a]
        arcs = []
        abgraph = AbstractGraph(nodes, arcs)
        BPMNModel = AbsToBPMNGraph(nodes, arcs)
        new_nodes, new_arcs = BPMNModel.transfor_all_nodes()
        print('------------BPMN---------------')
        print('BPMN nodes:', len(new_nodes))
        print(new_nodes)
        print([node.get_ident() for node in new_nodes])
        print('BPMN arcs:', len(new_arcs))
        print([arc.get_ident() for arc in new_arcs])
        print('-------------------------------')

        pytopif = Py2Pif(test)
        pytopif.getPIFXML(new_nodes, new_arcs)
        print("aaah")


if __name__ == "__main__":
    test = TestBPMN()
    # test.test_compute()
    # test.test_bpmn()
    # test.test_pif_simple()
    test.test_pif()
