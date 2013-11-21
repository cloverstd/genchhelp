# coding: utf-8

def cal_credit(credit_list):

    return reduce(lambda x, y: x+y, [float(i[1]) for i in credit_list])
