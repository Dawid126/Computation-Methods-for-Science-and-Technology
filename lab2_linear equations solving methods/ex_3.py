import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


def read_graph(path):
    return nx.read_edgelist(path, data=[('E', float), ('r', float)], create_using=nx.DiGraph, nodetype=int)


def label_edges(directed_graph):
    next_id = 0
    for e, attributes in directed_graph.edges.items():
        attributes['id'] = next_id
        next_id = next_id + 1
    return next_id


def format_edge(attributes):
    s = ""
    if 'id' in attributes:
        s = s + '({}) '.format(attributes['id'])
    if 'r' in attributes:
        s = s + '{:.2e}Ω\n'.format(attributes['r'])
    if 'E' in attributes:
        s = s + '{:.2e}V '.format(attributes['E'])
    if 'i' in attributes:
        s = s + '\n{:.2e}A '.format(attributes['i'])
    return s


def edge_direction(directed_graph, e):
    v1, v2 = e
    if e in directed_graph.edges:
        return True, directed_graph.edges[e]
    else:
        return False, directed_graph.edges[(v2, v1)]


def cycle_nodes_to_edges(cycle):
    return list(zip(cycle, cycle[1:] + cycle[0:1]))


def create_equation(directed_graph, num_of_unknowns):
    undirected_graph = directed_graph.to_undirected()
    cycles = [cycle_nodes_to_edges(cycle_nodes)
              for cycle_nodes in nx.cycle_basis(undirected_graph)]

    A = np.empty((0, num_of_unknowns))
    B = np.empty((0, 1))

    for node_pairs in cycles:
        E = sum_E(directed_graph, node_pairs)
        B = np.append(B, [[E]], axis=0)

        A_row = np.zeros((1, num_of_unknowns))
        for node_pair in node_pairs:
            correct, edge = edge_direction(directed_graph, node_pair)
            if correct:
                A_row[0][edge['id']] = A_row[0][edge['id']] + edge['r']
            else:
                A_row[0][edge['id']] = A_row[0][edge['id']] - edge['r']

        A = np.append(A, A_row, axis=0)

    for v in directed_graph.nodes:
        h, w = A.shape
        if w == h:
            break

        A_row = np.zeros((1, A.shape[1]))
        for e in directed_graph.in_edges(v):
            id = directed_graph.edges[e]['id']
            A_row[0][id] = A_row[0][id] + 1

        for e in directed_graph.out_edges(v):
            id = directed_graph.edges[e]['id']
            A_row[0][id] = A_row[0][id] - 1
        if np.allclose(A_row, 0, atol=1e-30):
            continue

        B = np.append(B, [[0]], axis=0)
        A = np.append(A, A_row, axis=0)

    return A, B


def sum_E(directed_graph, nodepairs):
    total_sum = 0
    for v1v2 in nodepairs:
        correct, attributes = edge_direction(directed_graph, v1v2)
        if correct:
            total_sum = total_sum + attributes['E']
        else:
            total_sum = total_sum + attributes['E']

    return total_sum


def add_results(directed_graph):
    to_add = []
    to_remove = []

    for e in directed_graph.edges:
        id = directed_graph.edges[e]['id']
        print(id)
        i = solved[0][id][0]

        v1, v2 = e
        if i < 0:
            attributes = directed_graph[v1][v2]
            attributes['i'] = -i
            attributes['E'] = attributes['E']
            to_remove = to_remove + [(v1, v2)]
            to_add = to_add + [(v2, v1, attributes)]
        else:
            directed_graph[v1][v2]['i'] = i
    directed_graph.remove_edges_from(to_remove)
    directed_graph.add_edges_from(to_add)


def format_results(directed_graph):
    edges = directed_graph.edges.items()
    return "\n".join(["{} {} {}".format(v1, v2, attributes['i']) for ((v1, v2), attributes) in sorted(edges)])


def draw_graph(graph, file, *, pos=None):
    pos = pos if pos else nx.spring_layout(graph)
    labels = {e: format_edge(attributes) for e, attributes in graph.edges.items()}

    plt.figure(figsize=(15,15))
    nx.draw_networkx(graph, pos=pos, with_labels=True, figsize=(15, 15))
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.tight_layout()
    plt.savefig(file)
    #print("Written figure {}".format(file), file=sys.stderr)
    plt.close()

    return pos


path = "in1.ssv"
directed_graph = read_graph(path)

num_of_unknowns = label_edges(directed_graph)
positions = draw_graph(directed_graph, "in1.png")

A, B = create_equation(directed_graph, num_of_unknowns)
print(B)
solved = np.linalg.lstsq(A, B)
print(solved)
print(solved[0][1][0])
add_results(directed_graph)
draw_graph(directed_graph, "out1.png", pos=positions)
formated = format_results(directed_graph)

print(formated)
result_file = open(r"result1.txt", "a+")
result_file.writelines(formated)