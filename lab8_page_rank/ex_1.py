import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import copy

n = 20
d = 1 #dla wartosci mniejszych niz 1 wszystkie wartosci w pagerank values zbiegaja do 0, dla wartosci wiekszej niz 1
      #wartosci w pagerank values powoduje overflow, dla 1 wyniki z obu metod sa takie same
eps = 10 ** (-10)

def compute_r_from_sum(matrix, num_of_nodes, d, eps):
    pr_values = np.full(num_of_nodes, 1 / num_of_nodes)
    while(True):
        old_pr_values = pr_values.copy()
        for j in range(num_of_nodes):
            sum = 0
            for i in range(num_of_nodes):
                if(matrix[i, j] != 0):
                    N_v = np.count_nonzero(matrix[i])
                    sum = sum + old_pr_values[i] / N_v
            pr_values[j] = d * sum

        if(np.linalg.norm(pr_values - old_pr_values) < eps):
            return pr_values


def compute_r_from_exponent_method(matrix, num_of_nodes, max_iterations, eps):
    old_pr_values = np.full((num_of_nodes, 1), 1 / num_of_nodes)
    old_pr_values = old_pr_values / np.linalg.norm(old_pr_values, 1)

    for i in range(max_iterations):
        pr_values = matrix.dot(old_pr_values)
        if (np.linalg.norm(pr_values - old_pr_values, 1) < eps):
            return pr_values

        old_pr_values = pr_values

    return pr_values

def transform_matrix(matrix):
    A = copy.deepcopy(matrix)
    A = A.transpose()

    for j in range(n):
        N_u = 0
        for i in range(n):
            if (A[i, j] != 0):
                N_u = N_u + 1
        for i in range(n):
            if (A[i, j] != 0):
                A[i, j] = 1 / N_u
    A = A * d
    return A

def draw_graph(G):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(15,15))
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_edges(G, pos, arrows=True)
    plt.plot()
    plt.show()


G = nx.random_k_out_graph(n, 4, 15, self_loops=False, seed=None)
adj_matrix = nx.to_numpy_matrix(G)
A = transform_matrix(adj_matrix)

pr1 = compute_r_from_exponent_method(A, n, 100, eps)
pr2 = compute_r_from_sum(adj_matrix, n, d, eps)

print("PageRank from matrix method:")
print(pr1.flatten(), end='\n\n')
print("PageRank from sum method:")
print(pr2)

#draw_graph(G)





