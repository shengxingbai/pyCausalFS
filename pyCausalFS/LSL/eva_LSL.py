# coding=utf-8
# /usr/bin/env python
"""
date: 2019/7/18 15:38
desc:
"""
import numpy as np
import pandas as pd
from LSL.MBs.common.real_P_C_S import real_p_c_s
from LSL.MBs.PCDbyPCD import PCDbyPCD
from LSL.MBs.MBbyMB import MBbyMB
from LSL.MBs.CMB.CMB import CMB


def evaluation(method,
               path,
               all_number_Para,
               target_list,
               real_graph_path,
               is_discrete,
               filenumber=10,
               alaph=0.01,
               ):
    # pre_set variables is zero
    length_target_list = len(target_list)
    real_p, real_c, real_s = real_p_c_s(all_number_Para, real_graph_path)
    num_re, num_undirect = 0, 0
    num_miss ,num_extra= 0, 0
    num_true = 0
    for m in range(filenumber):
        completePath = path + str(m + 1) + ".csv"
        data = pd.read_csv(completePath)
        get_p, get_c, get_un = [[]] * length_target_list, [[]] * \
            length_target_list, [[]] * length_target_list
        # print(get_p)
        for i, target in enumerate(target_list):
            if method == "PCDbyPCD":
                P, c, undirected = PCDbyPCD(data, target, alaph, is_discrete)
            elif method == "MBbyMB":
                P, c, undirected = MBbyMB(data, target, alaph, is_discrete)
            elif method == "CMB":
                P, c, undirected = CMB(data, target, alaph, is_discrete)
            else:
                raise Exception("method input error!")
            get_p[i] = P
            get_c[i] = c
            get_un[i] = undirected

        for n, target in enumerate(target_list):

            true_diection = list((set(real_p[target]).intersection(set(get_p[n]))).union(set(real_c[target]).intersection(set(get_c[n]))))
            num_true += len(true_diection)

            reverse_direction = list((set(real_p[target]).intersection(
                set(get_c[n]))).union(set(real_c[target]).intersection(set(get_p[n]))))
            num_re += len(reverse_direction)

            undirected_direction = list(get_un[n])
            num_undirect += len(undirected_direction)

            miss_direction = list(((set(real_p[target]).difference(set(get_p[n]))).union(
                set(real_c[target]).difference(set(get_c[n])))).difference(set(reverse_direction).union(undirected_direction)))
            num_miss += len(miss_direction)

            extra_direction = list(((set(get_p[n]).difference(real_p[target])).union(
                set(get_c[n]).difference(set(real_c[target])))))
            num_extra += len(extra_direction)
    commonDivisor = length_target_list * filenumber

    return num_true / commonDivisor, num_re / commonDivisor, num_miss / commonDivisor, num_extra / commonDivisor


# test main
if __name__ == '__main__':
    method_list = ["PCDbyPCD"]
    for method in method_list:
        # method = "IAMB"
        K_flag = True
        data = pd.read_csv('../CBD/data/Alarm1_s1000_v1.csv')
        _, num_para = np.shape(data)
        data_path = "../CBD/data/Alarm1_s1000_v"
        real_graph_path = "../CBD/data/Alarm1_graph.txt"
        list_target = [i for i in range(num_para)]
        isdiscrete = True
        file_number = 10

        alpha = 0.01
    print("\n")
    num_true, num_re, num_miss, num_extra = evaluation(
        method, data_path, num_para, list_target, real_graph_path, isdiscrete, file_number, alpha)
    print("true direction is: " + str(num_true))
    print("reverse is: " + str(num_re))
    print("miss is: " + str(num_miss))
    print("extra is: " + str(num_extra))

    with open(r".\output\outputLSL.txt", "w") as file:
        file.write(str(method) + ": \n")
        file.write("true direction is: " + str(num_true) + "\n")
        file.write("reverse is: " + str(num_re) + "\n")
        file.write("miss is: " + str(num_miss) + "\n")
        file.write("extra is: " + str(num_extra) + "\n")

