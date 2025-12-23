import heapq
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple


@dataclass(order=True)
class HeapItem:
    distance: int
    node: str = field(compare=False)


class Graph:
    def __init__(self) -> None:
        """Initialize an empty weighted graph."""
        self.adjacency: Dict[str, List[Tuple[str, int]]] = {}

    def add_edge(self, source: str, target: str, weight: int, bidirectional: bool = False) -> None:
        """Add an edge to the graph, optionally bidirectional."""
        self.adjacency.setdefault(source, []).append((target, weight))
        if bidirectional:
            self.adjacency.setdefault(target, []).append((source, weight))

    def dijkstra(self, start: str) -> Tuple[Dict[str, int], Dict[str, Optional[str]]]:
        """Compute shortest paths from a start node using a binary heap."""
        distances: Dict[str, int] = {node: float("inf") for node in self.adjacency}
        previous_nodes: Dict[str, Optional[str]] = {node: None for node in self.adjacency}
        distances[start] = 0
        heap: List[HeapItem] = [HeapItem(distance=0, node=start)]
        visited_nodes: set[str] = set()

        while heap:
            current_item = heapq.heappop(heap)
            current_node = current_item.node
            if current_node in visited_nodes:
                continue
            visited_nodes.add(current_node)

            for neighbor, weight in self.adjacency.get(current_node, []):
                new_distance = distances[current_node] + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(heap, HeapItem(distance=new_distance, node=neighbor))

        return distances, previous_nodes

    def shortest_path(self, start: str, end: str) -> List[str]:
        """Reconstruct the shortest path between two nodes after running Dijkstra."""
        distances, previous_nodes = self.dijkstra(start)
        if distances.get(end, float("inf")) == float("inf"):
            return []
        path: List[str] = []
        current_node: Optional[str] = end
        while current_node is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]
        path.reverse()
        return path


class GraphDemo:
    def __init__(self) -> None:
        """Prepare a demo graph with sample weighted edges."""
        self.graph = Graph()
        self._load_edges()

    def _load_edges(self) -> None:
        """Load a sample dataset into the graph."""
        edges: Iterable[Tuple[str, str, int]] = [
            ("A", "B", 4),
            ("A", "C", 2),
            ("B", "C", 5),
            ("B", "D", 10),
            ("C", "E", 3),
            ("E", "D", 4),
            ("D", "F", 11),
        ]
        for source, target, weight in edges:
            self.graph.add_edge(source, target, weight, bidirectional=True)

    def run(self) -> None:
        """Run Dijkstra on the demo graph and print distances."""
        distances, _ = self.graph.dijkstra("A")
        print("Shortest distances from A:")
        for node_name, distance in distances.items():
            print(f"{node_name}: {distance}")


if __name__ == "__main__":
    demo = GraphDemo()
    demo.run()
