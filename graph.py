from PIL import Image
import numpy as np


class Graph:
    def __init__(self, source, max_value):
        self.graph = np.array(Image.open(source))
        self.rev_graph = self.__reverse_values(max_value)
        self.heuristics = np.full((self.graph.shape[0], self.graph.shape[1]), np.inf)

    def __reverse_values(self, max_value):
        result = np.full((self.graph.shape[0], self.graph.shape[1]), np.inf)
        for y in range(self.graph.shape[0]):
            for x in range(self.graph.shape[1]):
                value = self.__node_value([x, y])
                if value == 0:
                    value = np.inf
                else:
                    gap_to_center = abs(max_value / 2 - value)
                    if max_value / 2 > value:
                        value += 2 * gap_to_center
                    else:
                        value -= 2 * gap_to_center
                result[y, x] = value
        return result

    def __node_value(self, node):
        val = 0
        for i in range(self.graph.shape[2]):
            val += self.graph[node[1], node[0], i]
        return val

    def set_heuristics(self, target):
        for y in range(self.rev_graph.shape[0]):
            for x in range(self.rev_graph.shape[1]):
                if self.rev_graph[y, x] == np.inf:
                    self.heuristics[y, x] = np.inf
                else:
                    horizontal = abs(target[1] - y)
                    vertical = abs(target[0] - x)
                    self.heuristics[y, x] = np.sqrt(pow(horizontal, 2) + pow(vertical, 2))
