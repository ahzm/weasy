# /usr/bin/env python3
# -*- coding:utf-8 -*-
# author: Ahang
# update: June 05, 2021


import xml.etree.ElementTree as ET
import os
from xml.dom import minidom
import random
import string
from basic_class import *
from partial_order import *
from abstract_graph import *
from bpmn_class import *


class Behaviour:

    def __init__(self, nodes, arcs, pif_behaviour):
        self.nodes = nodes
        self.arcs = arcs
        self.pif_behaviour = pif_behaviour
        self.generate_nodes()
        self.generate_arcs()

    def generate_nodes(self):

        for node in self.nodes:
            if isinstance(node, Activity):
                pif_nodes = ET.SubElement(self.pif_behaviour, "pif:nodes")
                pif_nodes.attrib = {"id": node.get_ident(),
                                    "xsi:type": "pif:Task"}

                for arc in self.arcs:
                    if arc.get_source_node() == node:
                        pif_outgoingFlows = ET.SubElement(
                            pif_nodes, "pif:outgoingFlows")
                        pif_outgoingFlows.text = arc.get_ident()
                    if arc.get_target_node() == node:
                        pif_incomingFlows = ET.SubElement(
                            pif_nodes, "pif:incomingFlows")
                        pif_incomingFlows.text = arc.get_ident()

            if isinstance(node, ParalNode):
                if 'start_parallel' in node.get_ident():
                    pif_nodes = ET.SubElement(self.pif_behaviour, "pif:nodes")
                    pif_nodes.attrib = {"id": node.get_ident(),
                                        "xsi:type": "pif:AndSplitGateway"}
                    for arc in self.arcs:
                        if arc.get_source_node() == node:
                            pif_outgoingFlows = ET.SubElement(
                                pif_nodes, "pif:outgoingFlows")
                            pif_outgoingFlows.text = arc.get_ident()
                        if arc.get_target_node() == node:
                            pif_incomingFlows = ET.SubElement(
                                pif_nodes, "pif:incomingFlows")
                            pif_incomingFlows.text = arc.get_ident()

                if 'end_parallel' in node.get_ident():
                    pif_nodes = ET.SubElement(self.pif_behaviour, "pif:nodes")
                    pif_nodes.attrib = {"id": node.get_ident(),
                                        "xsi:type": "pif:AndJoinGateway"}
                    for arc in self.arcs:
                        if arc.get_source_node() == node:
                            pif_outgoingFlows = ET.SubElement(
                                pif_nodes, "pif:outgoingFlows")
                            pif_outgoingFlows.text = arc.get_ident()
                        if arc.get_target_node() == node:
                            pif_incomingFlows = ET.SubElement(
                                pif_nodes, "pif:incomingFlows")
                            pif_incomingFlows.text = arc.get_ident()

            if isinstance(node, ExcluNode):
                if 'exclusive_split' in node.get_ident():
                    pif_nodes = ET.SubElement(self.pif_behaviour, "pif:nodes")
                    pif_nodes.attrib = {"id": node.get_ident(),
                                        "xsi:type": "pif:XOrSplitGateway"}
                    print(node.get_ident())
                    for arc in self.arcs:
                        if arc.get_source_node() == node:
                            pif_outgoingFlows = ET.SubElement(
                                pif_nodes, "pif:outgoingFlows")
                            pif_outgoingFlows.text = arc.get_ident()
                        if arc.get_target_node() == node:
                            pif_incomingFlows = ET.SubElement(
                                pif_nodes, "pif:incomingFlows")
                            pif_incomingFlows.text = arc.get_ident()

                if 'exclusive_merge' in node.get_ident():
                    #print('yes exlu merge')
                    pif_nodes = ET.SubElement(self.pif_behaviour, "pif:nodes")
                    pif_nodes.attrib = {"id": node.get_ident(),
                                        "xsi:type": "pif:XOrJoinGateway"}
                    for arc in self.arcs:
                        if arc.get_source_node() == node:
                            pif_outgoingFlows = ET.SubElement(
                                pif_nodes, "pif:outgoingFlows")
                            pif_outgoingFlows.text = arc.get_ident()
                        if arc.get_target_node() == node:
                            pif_incomingFlows = ET.SubElement(
                                pif_nodes, "pif:incomingFlows")
                            pif_incomingFlows.text = arc.get_ident()

            if isinstance(node, Start):

                pif_initialNode = ET.SubElement(
                    self.pif_behaviour, "pif:initialNode")
                pif_initialNode.text = node.get_ident()

                pif_nodes = ET.SubElement(self.pif_behaviour, "pif:nodes")
                pif_nodes.attrib = {"id": node.get_ident(),
                                    "xsi:type": "pif:InitialEvent"}
                for arc in self.arcs:
                    if arc.get_source_node() == node:
                        pif_outgoingFlows = ET.SubElement(
                            pif_nodes, "pif:outgoingFlows")
                        pif_outgoingFlows.text = arc.get_ident()
                    if arc.get_target_node() == node:
                        pif_incomingFlows = ET.SubElement(
                            pif_nodes, "pif:incomingFlows")
                        pif_incomingFlows.text = arc.get_ident()

            if isinstance(node, End):
                pif_finalNodes = ET.SubElement(
                    self.pif_behaviour, "pif:finalNodes")
                pif_finalNodes.text = node.get_ident()

                pif_nodes = ET.SubElement(self.pif_behaviour, "pif:nodes")
                pif_nodes.attrib = {"id": node.get_ident(),
                                    "xsi:type": "pif:EndEvent"}
                for arc in self.arcs:
                    if arc.get_source_node() == node:
                        pif_outgoingFlows = ET.SubElement(
                            pif_nodes, "pif:outgoingFlows")
                        pif_outgoingFlows.text = arc.get_ident()
                    if arc.get_target_node() == node:
                        pif_incomingFlows = ET.SubElement(
                            pif_nodes, "pif:incomingFlows")
                        pif_incomingFlows.text = arc.get_ident()

    def generate_arcs(self):
        for arc in self.arcs:
            pif_sequenceFlows = ET.SubElement(
                self.pif_behaviour, "pif:sequenceFlows")
            pif_sequenceFlows.attrib = {"id": arc.get_ident(),
                                        "source": arc.get_source_node().get_ident(),
                                        "target": arc.get_target_node().get_ident()
                                        }


class Py2Pif:

    def __init__(self, name, documentation=""):
        self.pif_process, self.pif_behaviour = self.genrate_process()
        self.pif_name = name
        self.pif_documentation = documentation

    def genrate_process(self):

        self.pif_process = ET.Element("pif:Process")  # 创建根节点

        self.pif_process.attrib = {
            "xmlns:pif": "http://www.example.org/PIF",
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
            "xsi:schemaLocation": "http://www.example.org/PIF ../pif.xsd"
        }

        self.pif_name = ET.SubElement(self.pif_process, "pif:name")
        self.pif_name.text = "test"

        self.pif_documentation = ET.SubElement(
            self.pif_process, "pif:documentation")

        self.pif_behaviour = ET.SubElement(self.pif_process, "pif:behaviour")

        return self.pif_process, self.pif_behaviour

    def generate_behaviour(self, nodes, arcs):
        Behaviour(nodes, arcs, self.pif_behaviour)

    def getPIFXML(self, nodes, arcs):
        self.generate_behaviour(nodes, arcs)
        tree = ET.ElementTree(self.pif_process)  # 创建elementtree对象，写文件
        name = ''.join(random.choice(string.ascii_letters) for i in range(8))
        #print(os.path.dirname(os.path.abspath(__file__)))
        tree.write(os.path.join(os.path.dirname(os.path.abspath(
            __file__)),  name+'.pif'), 'UTF-8', xml_declaration=True)
        return os.path.dirname(os.path.abspath(__file__)), name+".pif"
