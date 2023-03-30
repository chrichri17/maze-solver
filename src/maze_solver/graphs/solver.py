import networkx as nx

from maze_solver.graphs.converter import make_graph
from maze_solver.models.maze import Maze
from maze_solver.models.solution import Solution


def solve(maze: Maze) -> Solution | None:
    try:
        return Solution(
            squares=tuple(
                nx.shortest_path(
                    make_graph(maze),
                    source=maze.entrance,
                    target=maze.exit,
                )
            )
        )
    except nx.NetworkXException:
        return None
