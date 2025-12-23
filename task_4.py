import uuid
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx


@dataclass
class Node:
    value: int
    color: str = "skyblue"
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    node_id: str = ""

    def __post_init__(self) -> None:
        """Assign a unique identifier after initialization."""
        self.node_id = str(uuid.uuid4())


class BinaryHeap:
    def __init__(self, values: List[int]) -> None:
        """Initialize the heap from a list of values."""
        self.values = values

    def to_tree(self) -> Optional[Node]:
        """Convert the heap array into a binary tree of Nodes."""
        if not self.values:
            return None
        nodes = [Node(value=value) for value in self.values]
        for index, node in enumerate(nodes):
            left_index = 2 * index + 1
            right_index = 2 * index + 2
            if left_index < len(nodes):
                node.left = nodes[left_index]
            if right_index < len(nodes):
                node.right = nodes[right_index]
        return nodes[0]


class HeapVisualizer:
    def __init__(self) -> None:
        """Initialize the graph visualizer for binary trees."""
        self.graph = nx.DiGraph()

    def _add_edges(
        self,
        node: Optional[Node],
        positions: Dict[str, Tuple[float, float]],
        horizontal_pos: float = 0.0,
        vertical_pos: float = 0.0,
        layer_number: int = 1,
    ) -> None:
        """Recursively add nodes and edges to the graph."""
        if node is None:
            return
        self.graph.add_node(node.node_id, color=node.color, label=node.value)
        if node.left:
            self.graph.add_edge(node.node_id, node.left.node_id)
            left_pos = horizontal_pos - 1 / 2 ** layer_number
            positions[node.left.node_id] = (left_pos, vertical_pos - 1)
            self._add_edges(node.left, positions, left_pos, vertical_pos - 1, layer_number + 1)
        if node.right:
            self.graph.add_edge(node.node_id, node.right.node_id)
            right_pos = horizontal_pos + 1 / 2 ** layer_number
            positions[node.right.node_id] = (right_pos, vertical_pos - 1)
            self._add_edges(node.right, positions, right_pos, vertical_pos - 1, layer_number + 1)

    def draw(self, root: Node) -> None:
        """Draw the binary tree using matplotlib."""
        positions: Dict[str, Tuple[float, float]] = {root.node_id: (0.0, 0.0)}
        self._add_edges(root, positions)
        colors = [node[1]["color"] for node in self.graph.nodes(data=True)]
        labels = {node[0]: node[1]["label"] for node in self.graph.nodes(data=True)}

        plt.figure(figsize=(8, 5))
        nx.draw(self.graph, pos=positions, labels=labels, arrows=False, node_size=2500, node_color=colors)
        plt.show()


class HeapDemo:
    def __init__(self) -> None:
        """Prepare a demo heap to visualize."""
        self.heap = BinaryHeap([0, 4, 1, 5, 10, 3])

    def run(self) -> None:
        """Convert the heap to a tree and draw it."""
        root = self.heap.to_tree()
        if root is None:
            print("Heap is empty.")
            return
        visualizer = HeapVisualizer()
        visualizer.draw(root)


if __name__ == "__main__":
    demo = HeapDemo()
    demo.run()
