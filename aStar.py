import numpy as np


def _reconstruct_path(ancestors, current_node, start_node):
    path = [current_node]
    ancestor = ancestors.get(tuple(current_node))
    path.append(ancestor)
    while ancestor != start_node:
        ancestor = ancestors.get(tuple(ancestor))
        path.append(ancestor)
    path.reverse()
    return path


def _best_node(nodes, values):
    hash_map = {}
    for node in nodes:
        hash_map[tuple(node)] = values[node[1], node[0]]
    val = np.inf
    lowest_key = None
    for key in hash_map:
        if hash_map[key] <= val:
            val = hash_map[key]
            lowest_key = key
    return list(lowest_key)


def _find_neighbours(graph, current_node):
    north_flag = False
    west_flag = False
    south_flag = False
    east_flag = False
    neighbours = []
    x = current_node[0]
    y = current_node[1]
    if y > 0:
        north_flag = True
        neighbours.append([x, y - 1])
    if x < graph.shape[1] - 1:
        west_flag = True
        neighbours.append([x + 1, y])
    if y < graph.shape[0] - 1:
        south_flag = True
        neighbours.append([x, y + 1])
    if x > 0:
        east_flag = True
        neighbours.append([x - 1, y])
    if north_flag and west_flag:
        neighbours.append([x + 1, y - 1])
    if west_flag and south_flag:
        neighbours.append([x + 1, y + 1])
    if south_flag and east_flag:
        neighbours.append([x - 1, y + 1])
    if east_flag and north_flag:
        neighbours.append([x - 1, y - 1])
    return neighbours


def _calculate_edge(from_node, to_node):
    horizontal = abs(from_node[0] - to_node[0])
    vertical = abs(from_node[1] - to_node[1])
    return np.sqrt(pow(horizontal, 2) + pow(vertical, 2))


# node -> n
# f(n) = g(n) + h(n)
# f(n) -> f_value[n]
# g(n) -> g_value[n]
# n -> [x, y]
def calculate(start_node, target_node, graph, heuristics):
    if heuristics[target_node[1], target_node[0]] == np.inf:
        return []
    if heuristics[start_node[1], start_node[0]] == np.inf:
        return []

    open_set = [start_node]
    ancestors = {}
    g_value = np.full((graph.shape[0], graph.shape[1]), np.inf)
    g_value[start_node[1], start_node[0]] = 0
    f_value = np.full((graph.shape[0], graph.shape[1]), np.inf)
    f_value[start_node[1], start_node[0]] = heuristics[start_node[1], start_node[0]]

    while open_set:
        current_node = _best_node(open_set, f_value)
        if current_node == target_node:
            return _reconstruct_path(ancestors, current_node, start_node)
        open_set.remove(current_node)
        for neighbour in _find_neighbours(graph, current_node):
            new_g_value = \
                g_value[current_node[1], current_node[0]] + _calculate_edge(current_node, neighbour)
            if new_g_value < g_value[neighbour[1], neighbour[0]]:
                ancestors[tuple(neighbour)] = current_node
                g_value[neighbour[1], neighbour[0]] = new_g_value
                f_value[neighbour[1], neighbour[0]] = \
                    g_value[neighbour[1], neighbour[0]] + heuristics[neighbour[1], neighbour[0]]
                if neighbour not in open_set:
                    open_set.append(neighbour)
    return []
