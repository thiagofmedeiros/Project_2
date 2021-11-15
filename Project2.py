import sys
import argparse
from Graph import Graph


def main():
    # Parse arguments into file names
    parser = argparse.ArgumentParser()
    parser.add_argument('inputFile')
    parser.add_argument('outputFile')

    args = parser.parse_args()

    # Init graph from input file
    graph = Graph(args.inputFile)

    # Find path from first vertex to last vertex
    path = graph.find_path(0, graph.numberVertex)

    # Print path from graph into output file
    graph.print_path(path, args.outputFile)

    return 0


if __name__ == '__main__':
    sys.exit(main())
