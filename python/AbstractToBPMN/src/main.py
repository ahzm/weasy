# /usr/bin/env python3
# -*- coding:utf-8 -*-
# author: Ahang
# update: Jan 05, 2021

"""
"""

from test_class import *


def main(num=1):
    if num == 1:  # test: partial order
        test_po = TestPartialOrder()
        test_po.test_partial_order()

    if num == 2:  # test: abstract graph, bpmn
        test = TestBPMN()
        test.test_bpmn()
        test.test_pif()
    if num == 3:  # test: autotest paper
        autotest = AutoTest()
        autotest.test_cases()


if __name__ == "__main__":
    main(2)
