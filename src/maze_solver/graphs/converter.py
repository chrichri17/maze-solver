import math

from typing import NamedTuple, TypeAlias

import networkx as nx

from maze_solver.models.border import Border
from maze_solver.models.maze import Maze
from maze_solver.models.role import Role
from maze_solver.models.square import Square

Node: TypeAlias = Square


class Edge(NamedTuple):
    node1: Node
    node2: Node

    @property
    def distance(self) -> float:
        return math.dist(
            (self.node1.row, self.node1.column),
            (self.node2.row, self.node2.column),
        )


def make_graph(maze: Maze) -> nx.Graph:
    return nx.Graph(
        (edge.node1, edge.node2, {"weight": edge.distance})
        for edge in get_edges(maze, get_nodes(maze))
    )


def get_nodes(maze: Maze) -> set[Node]:
    nodes: set[Node] = set()

    for square in maze:
        if square.role in (Role.EXTERIOR, Role.WALL):
            continue
        if square.role is not Role.NONE:
            nodes.add(square)
        if (
            square.border.intersection
            or square.border.dead_end
            or square.border.corner
        ):
            nodes.add(square)

    return nodes


def get_edges(maze: Maze, nodes: set[Node]) -> set[Edge]:
    edges: set[Edge] = set()

    for source_node in nodes:
        # Follow right
        node = source_node
        for x in range(node.column + 1, maze.width):
            if node.border & Border.RIGHT:
                break
            node = maze[node.row * maze.width + x]
            if node in nodes:
                edges.add(Edge(source_node, node))
                break

        # Follow down
        node = source_node
        for y in range(node.row + 1, maze.height):
            if node.border & Border.BOTTOM:
                break
            node = maze[y * maze.width + node.column]
            if node in nodes:
                edges.add(Edge(source_node, node))
                break

    return edges
