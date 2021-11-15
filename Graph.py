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

    def __init__(self, inputFile):
        self.graph = defaultdict(list)
        self.colors, self.directions = self.readFile(inputFile)
        self.rows = self.colors.shape[0]
        self.columns = self.colors.shape[1]
        self.numberVertices = self.rows * self.columns - 1

        self.createGraph()

    def printPath(self, path, outputFile):
        outputFile = open(outputFile, 'w')

        i = 0

        while i < len(path):
            for node in self.graph[path[i]]:
                if node[0] == path[i + 1]:
                    outputFile.write("{0}{1} ".format(node[1], node[2]))
            i += 1

        outputFile.close()

    def findPath(self, start, end, pathIndex=None):
        if pathIndex is None:
            pathIndex = []

        pathIndex = pathIndex + [start]

        if start == end:
            return pathIndex

        for node in self.graph[start]:
            if node[0] not in pathIndex:
                newpath = self.findPath(node[0], end, pathIndex)

                if newpath:
                    return newpath
        return None

    def addEdge(self, src, dest, weight, direction):
        newNode = [dest, weight, direction]
        self.graph[src].insert(0, newNode)

    def createGraph(self):
        for rowInit in range(self.rows):
            for columnInit in range(self.columns):
                self.walkDirection(rowInit, columnInit)

    def walkDirection(self, rowInit, columnInit):
        source = rowInit * self.columns + columnInit
        weight = 1
        direction = self.directions[rowInit][columnInit]
        color = self.colors[rowInit][columnInit]

        if direction == NORTH:
            i = rowInit - 1
            j = columnInit

            while i >= 0:
                if self.colors[i, j] != color:
                    dest = i * self.columns + j
                    self.addEdge(source, dest, weight, direction)
                i -= 1
                weight += 1

        elif direction == SOUTH:
            i = rowInit + 1
            j = columnInit

            while i < self.rows:
                if self.colors[i, j] != color:
                    dest = i * self.columns + j
                    self.addEdge(source, dest, weight, direction)
                i += 1
                weight += 1

        elif direction == WEST:
            i = rowInit
            j = columnInit - 1

            while j >= 0:
                if self.colors[i, j] != color:
                    dest = i * self.columns + j
                    self.addEdge(source, dest, weight, direction)
                j -= 1
                weight += 1

        elif direction == EAST:
            i = rowInit
            j = columnInit + 1

            while j < self.columns:
                if self.colors[i, j] != color:
                    dest = i * self.columns + j
                    self.addEdge(source, dest, weight, direction)
                j += 1
                weight += 1

        elif direction == NORTHEAST:
            i = rowInit - 1
            j = columnInit + 1

            while i >= 0 and j < self.columns:
                if self.colors[i, j] != color:
                    dest = i * self.columns + j
                    self.addEdge(source, dest, weight, direction)
                i -= 1
                j += 1
                weight += 1

        elif direction == NORTHWEST:
            i = rowInit - 1
            j = columnInit - 1

            while i >= 0 and j >= 0:
                if self.colors[i, j] != color:
                    dest = i * self.columns + j
                    self.addEdge(source, dest, weight, direction)
                i -= 1
                j -= 1
                weight += 1

        elif direction == SOUTHEAST:
            i = rowInit + 1
            j = columnInit + 1

            while i < self.rows and j < self.columns:
                if self.colors[i, j] != color:
                    dest = i * self.columns + j
                    self.addEdge(source, dest, weight, direction)
                i += 1
                j += 1
                weight += 1

        elif direction == SOUTHWEST:
            i = rowInit + 1
            j = columnInit - 1

            while i < self.rows and j >= 0:
                if self.colors[i, j] != color:
                    dest = i * self.columns + j
                    self.addEdge(source, dest, weight, direction)
                i += 1
                j -= 1
                weight += 1

    def readFile(self, inputFile):
        rows = 0
        columns = 0
        directions = np.zeros(1)
        colors = np.zeros(1)

        with open(inputFile, 'r') as file:
            notFirst = False
            i = 0
            for line in file:
                j = 0
                if notFirst:
                    for word in line.split():
                        if not (i == rows - 1 and j == columns - 1):
                            colors[i][j], directions[i][j] = word.split('-')
                        else:
                            colors[i][j] = 'O'
                            directions[i][j] = 'O'
                        j += 1
                    i += 1

                else:
                    rows, columns = line.split()
                    rows = int(rows)
                    columns = int(columns)

                    colors = np.full((rows, columns), '')
                    directions = np.full((rows, columns), '  ')
                notFirst = True

        return colors, directions
