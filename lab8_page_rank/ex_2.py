import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy

n = 1005
d = 0.85
eps = 10 ** (-10)

def compute_r_from_sum(matrix, num_of_nodes, e, d, eps):
    pr_values = np.full(num_of_nodes, 1 / num_of_nodes)
    while(True):
        old_pr_values = pr_values.copy()
        for j in range(num_of_nodes):
            sum = 0
            for i in range(num_of_nodes):
                if(matrix[i, j] != 0):
                    N_v = np.count_nonzero(matrix[i])
                    sum = sum + old_pr_values[i] / N_v
            pr_values[j] = d * sum + (1-d) * e[j]

        if(np.linalg.norm(pr_values - old_pr_values) < eps):
            return pr_values


def compute_r_from_exponent_method(matrix, num_of_nodes, max_iterations, e, eps):
    e = np.reshape(e, (num_of_nodes, 1))
    old_pr_values = np.full((num_of_nodes, 1), 1 / num_of_nodes)
    old_pr_values = old_pr_values / np.linalg.norm(old_pr_values, 1)

    for i in range(max_iterations):
        pr_values = matrix.dot(old_pr_values)

        d = np.linalg.norm(old_pr_values, 1) - np.linalg.norm(pr_values, 1)
        pr_values = pr_values + e * d

        if (np.linalg.norm(pr_values - old_pr_values, 1) < eps):
            return pr_values

        old_pr_values = pr_values

    return pr_values

def transform_matrix(matrix):
    B = copy.deepcopy(matrix)
    B = B.transpose()
    n = np.shape(B)[0]

    for j in range(n):
        N_u = 0
        for i in range(n):
            if (B[i, j] != 0):
                N_u = N_u + 1
        for i in range(n):
            if (B[i, j] != 0):
                B[i, j] = 1 / N_u

    return B

def draw_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(15,15))
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=True)
    plt.plot()
    plt.show()


def load_graph(path):
    DG = nx.DiGraph()
    f = open(path, 'r+')
    for edge in f.readlines():
        tuple = edge.split()
        DG.add_edge(tuple[0], tuple[1])

    return DG


#sprawdzanie czy algorytm dziala poprawnie dla malego grafu
G = nx.random_k_out_graph(20, 4, 15, self_loops=False, seed=None)
e = np.full(20, 1/20)
adj_matrix = nx.to_numpy_matrix(G)

B = d * transform_matrix(adj_matrix) + (1 - d) / n

pr1 = compute_r_from_exponent_method(B, 20, 100, e, eps)
pr2 = compute_r_from_sum(adj_matrix, 20, e, d, eps)

print("PageRank from matrix method:")
print(pr1.flatten(), end='\n\n')
print("PageRank from sum method:")
print(pr2)

#draw_graph(G)

#graf z SNAP
different_d = [0.9, 0.85, 0.75, 0.6, 0.5]
different_e =[]
tmp = np.random.rand(n, 1)
different_e.append(tmp / sum(tmp))
tmp = np.arange(1/n, 1, 1/n)
different_e.append((tmp / sum(tmp)).reshape((n,1)))
different_e.append(np.full(n, 1/n).reshape((n,1))) #tak aby suma wszystkich elementow e wynosila 1

DG = load_graph("email-Eu-core.txt")
adj_matrix = nx.to_numpy_matrix(DG)
B = transform_matrix(adj_matrix)

for ds in different_d:
    for i in range(3):
        B_new = d * B + (1-ds) / n
        pr1 = compute_r_from_exponent_method(B, n, 100, different_e[i], eps)

        print(f"PageRank from matrix method and d ={ds}, e ind={i}:")
        print(pr1.flatten(), end='\n\n')



