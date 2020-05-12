import cplex


def lp_solver(datas, systems, budget, preference, data_trans_size, init_values = None, time_limit = None, read_flag = False, write_flag = False, request_budget=True):
    
    
    num_of_clients = len(datas)
    num_of_class = len(datas[0])

    # Create the modeler/solver
    prob = cplex.Cplex()
    prob.objective.set_sense(prob.objective.sense.minimize)

    slowest = prob.variables.add(lb = [0.0], types = ['C'], names = ['slowest'])

    qlist = []
    qub = []
    for i in range(num_of_clients):
        for j in range(num_of_class):
            qlist.append('q' + str(i) + str(j))
            qub.append(datas[i][j])


    quantity = prob.variables.add(lb = [0.0] * num_of_clients * num_of_clients,
                                ub = qub,
                                types = ['I'] * num_of_clients * num_of_class,
                                names = qlist)

    trans_time = [round(data_trans_size/systems[i][1], 2) for i in range(num_of_clients)]
    speed = [systems[i][0]/1000. for i in range(num_of_clients)]


#datas = [[10, 20, 10, 1], [10, 19, 10, 1], [20, 15, 17, 20], [20, 30, 17, 10]]
#system = [5, 10, 15, 30]
#datas = [[100, 100, 100, 100], [100, 100, 100, 100], [100, 100, 100, 100], [100, 100, 100, 100]]
datas=[[40], [40], [40], [40]]
system = [5000, 10, 10, 10]
cost = [1, 1, 1, 1]
budget = 10
data_trans_size = 6
bw = [1, 1, 1, 1]
preference = [40]
lp_solver(datas, system, budget, cost, preference, bw, data_trans_size)