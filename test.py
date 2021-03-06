import pickle
import numpy as np
import gurobipy as gp
from gurobipy import *

def load_profiles(datafile, sysfile):
    # load user data information
    datas = pickle.load(open(datafile, 'rb'))

    # load user system information
    systems = None #pickle.load(open(sysfile, 'rb'))

    return datas, systems

def lp_solver(datas, systems, budget, cost, preference, bw, data_trans_size):

    num_of_clients = len(datas)
    num_of_class = len(datas[0])

    # Create a new model
    m = gp.Model("client_selection")

    qlist = []
    for i in range(num_of_clients):
        for j in range(num_of_class):
            qlist.append((i, j))

    slowest = m.addVar(vtype=GRB.CONTINUOUS, name="slowest", lb = 0.0)
    quantity = m.addVars(qlist, vtype=GRB.INTEGER, name="quantity", lb = 0) # # of example for each class
    status = m.addVars([i for i in range(num_of_clients)], vtype = GRB.BINARY, name = 'status') # Binary var indicates the selection status

    time_list = [((gp.quickSum([quantity[(i, j)] for j in range(num_of_class)])/systems[i]) + data_trans_size/bw[i]) for i in range(num_of_clients)]

    # The objective is to minimize the slowest
    m.setObjective(slowest, GRB.MINIMIZE)

    # Minimize the slowest
    for t in time_list:
        m.addConstr(slowest >= t, name='slow')

    # Preference Constraint
    for i in range(num_of_class):
        m.addConstr(gp.quickSum([quantity[(client, i)] for client in range(num_of_clients)]) >= preference[i], name='preference_' + str(i))

    # Capacity Constraint
    m.addConstrs((quantity[i] <= datas[i[0]][i[1]] for i in qlist), name='capacity_'+str(i))

    # Budget Constraint
    for i in range(num_of_clients):
        m.addGenConstrIndicator(status[i], False, gp.quickSum([quantity[(i, j)] for j in range(num_of_class)]) ==  0.0)

    m.addConstr(gp.quickSum([status[i] for i in range(num_of_clients)]) <= budget, name = 'budget')

    m.optimize()

    # Print Solution
    if m.status == GRB.OPTIMAL:
        print('Found solution')
        pointx = m.getAttr('x', quantity)
        for i in qlist:
            if quantity[i].x > 0.0001:
                print(i, pointx[i])
    else:
        print('No solution')



datas = [[10, 20, 10, 1], [0, 19, 0, 0], [0, 0, 1, 0], [0, 0, 1, 10]]
system = [10, 10, 17, 10]
bw = [2, 5, 5, 10]
data_trans_size = 5
cost = [1, 1, 1, 1]
budget = 3
preference = [10, 39, 11, 10]
lp_solver(datas, system, budget, cost, preference, bw, data_trans_size)

# def lp_heuristic():
#     datas, systems = load_profiles('openImg_size.txt', '')


#     # randomly generating preference
#     pref = [100, 100, 100, 100, 100]
#     p = [0] *6065

#     #pred = [ 0 for i in range(len(datas[0])-5)]
#     pref = pref + p
#     print(len(pref))
#     system = [i+1 for i in range(len(datas[0]))]
#     bw = []
#     budget = 5
#     data_trans_size = 5
#     cost = [1 for i in range(len(datas[0]))]
#     print(len(datas))
#     print(type(datas[0]))
#     lp_solver(datas[:100], system, budget, cost, pref, bw, data_trans_size)

# lp_heuristic()