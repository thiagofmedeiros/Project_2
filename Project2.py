import sys
import argparse
from Graph import Graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile')
    parser.add_argument('outputFile')

    args = parser.parse_args()

    graph = Graph(args.inputFile)

    path = graph.findPath(0, graph.numberVertices)

    graph.printPath(path, args.outputFile)

    return 0


if __name__ == '__main__':
    sys.exit(main())
