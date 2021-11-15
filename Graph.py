from collections import defaultdict

import numpy as np

NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'
NORTHEAST = 'NE'
NORTHWEST = 'NW'
SOUTHEAST = 'SE'
SOUTHWEST = 'SW'


class Graph:

    def __init__(self, input_file):
        self.graph = defaultdict(list)
        self.colors, self.directions = self.read_file(input_file)
        self.rows = self.colors.shape[0]
        self.columns = self.colors.shape[1]
        self.numberVertex = self.rows * self.columns - 1

        self.create_graph()

    # Print path directions and weights to an file
    def print_path(self, path, output_file):
        output_file = open(output_file, 'w')

        i = 0

        # Path is composed of list of vertex
        # Iterates through list of vertex in path to print it
        while i < len(path):
            # Search for edge from vertex that is in path and print its weight and direction
            for edge in self.graph[path[i]]:
                if edge[0] == path[i + 1]:
                    output_file.write("{0}{1} ".format(edge[1], edge[2]))
                    break
            i += 1

        output_file.close()

    # Recursion function to find a path between 2 vertex
    # The first time it is called, it has no path
    def find_path(self, start, end, path=None):
        if path is None:
            path = []

        # Add vertex to path
        path = path + [start]

        # Reached destination and return path
        if start == end:
            return path

        # Iterate through all edges from vertex
        for edge in self.graph[start]:
            # Verify if vertex is not on path to avoid cycles
            if edge[0] not in path:
                # recursive call until find destination
                new_path = self.find_path(edge[0], end, path)

                if new_path:
                    return new_path
        # No route found
        return None

    # Add edge with weight and direction to graph
    def add_edge(self, src, dest, weight, direction):
        new_edge = [dest, weight, direction]
        self.graph[src].insert(0, new_edge)

    # Iterate through rows and columns from file to create oriented graph
    # with possible walks
    def create_graph(self):
        for rowInit in range(self.rows):
            for columnInit in range(self.columns):
                self.walk_direction_color(rowInit, columnInit)

    # Adds edges to graph according to possible walks
    # given colors and directions in vertexes from file
    def walk_direction_color(self, row_init, column_init):
        # Creates source number
        source = row_init * self.columns + column_init
        # Inits weight of walk
        weight = 1
        # Get walk direction from source
        direction = self.directions[row_init][column_init]
        # Get source color
        source_color = self.colors[row_init][column_init]

        if direction == NORTH:
            # Direction NORTH only decreases row count
            i = row_init - 1
            j = column_init

            # Iterates until top of file is reached
            while i >= 0:
                self.verify_add_edge(i, j, source_color, source, weight, direction)
                i -= 1
                weight += 1

        elif direction == SOUTH:
            # Direction SOUTH only increases row count
            i = row_init + 1
            j = column_init

            # Iterates until bottom of file is reached
            while i < self.rows:
                self.verify_add_edge(i, j, source_color, source, weight, direction)
                i += 1
                weight += 1

        elif direction == WEST:
            # Direction WEST only decreases column count
            i = row_init
            j = column_init - 1

            # Iterates until left of file is reached
            while j >= 0:
                self.verify_add_edge(i, j, source_color, source, weight, direction)
                j -= 1
                weight += 1

        elif direction == EAST:
            # Direction EAST only increases column count
            i = row_init
            j = column_init + 1

            # Iterates until right of file is reached
            while j < self.columns:
                self.verify_add_edge(i, j, source_color, source, weight, direction)
                j += 1
                weight += 1

        elif direction == NORTHEAST:
            # Direction NORTHEAST
            # decreases row count
            # increases column count
            i = row_init - 1
            j = column_init + 1

            # Iterates until
            # top of file is reached
            # or
            # right of file is reached
            while i >= 0 and j < self.columns:
                self.verify_add_edge(i, j, source_color, source, weight, direction)
                i -= 1
                j += 1
                weight += 1

        elif direction == NORTHWEST:
            # Direction NORTHWEST
            # decreases row count
            # decreases column count
            i = row_init - 1
            j = column_init - 1

            # Iterates until
            # top of file is reached
            # or
            # left of file is reached
            while i >= 0 and j >= 0:
                self.verify_add_edge(i, j, source_color, source, weight, direction)
                i -= 1
                j -= 1
                weight += 1

        elif direction == SOUTHEAST:
            # Direction SOUTHEAST
            # increases row count
            # increases column count
            i = row_init + 1
            j = column_init + 1

            # Iterates until
            # bottom of file is reached
            # or
            # right of file is reached
            while i < self.rows and j < self.columns:
                self.verify_add_edge(i, j, source_color, source, weight, direction)
                i += 1
                j += 1
                weight += 1

        elif direction == SOUTHWEST:
            # Direction SOUTHWEST
            # increases row count
            # decreases column count
            i = row_init + 1
            j = column_init - 1

            # Iterates until
            # bottom of file is reached
            # or
            # left of file is reached
            while i < self.rows and j >= 0:
                self.verify_add_edge(i, j, source_color, source, weight, direction)
                i += 1
                j -= 1
                weight += 1

    # Verify if destination is valid and
    # adds to the graph
    def verify_add_edge(self, i, j, source_color, source, weight, direction):
        # Only adds edge if colors differ from each other
        if self.colors[i, j] != source_color:
            # Creates destination number
            dest = i * self.columns + j
            self.add_edge(source, dest, weight, direction)

    # Reads input file and creates
    # Color matrix and
    # Direction matrix
    @staticmethod
    def read_file(input_file):
        # Init variables
        rows = 0
        columns = 0
        directions = np.zeros(1)
        colors = np.zeros(1)
        not_first = False
        i = 0

        with open(input_file, 'r') as file:
            # Read each line in file
            for line in file:
                j = 0
                # Matrix data only if not in first line
                if not_first:
                    # Iterates between vertex
                    for word in line.split():
                        # Considering last element always different
                        # from color and direction
                        if not (i == rows - 1 and j == columns - 1):
                            # Separate color and direction into 2 matrix
                            colors[i][j], directions[i][j] = word.split('-')
                        # Last element as destination
                        else:
                            colors[i][j] = word
                            directions[i][j] = word
                        j += 1
                    i += 1

                # first line reads number of rows and columns
                # to create matrix
                else:
                    rows, columns = line.split()
                    rows = int(rows)
                    columns = int(columns)

                    colors = np.full((rows, columns), '')
                    directions = np.full((rows, columns), '  ')
                    not_first = True

        return colors, directions
