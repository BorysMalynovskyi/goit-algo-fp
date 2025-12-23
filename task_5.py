import uuid
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Iterable, List, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx


@dataclass
class Node:
    value: int
    color: str = "#1296f0"
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


class TreeBuilder:
    def __init__(self, values: List[int]) -> None:
        """Create a binary tree using the heap layout from task 4."""
        self.heap = BinaryHeap(values)

    def build(self) -> Node:
        """Return the root node of the tree."""
        root = self.heap.to_tree()
        if root is None:
            raise ValueError("Heap is empty.")
        return root


class ColorPalette:
    def __init__(self, start_color: Tuple[int, int, int], end_color: Tuple[int, int, int]) -> None:
        """Store the RGB endpoints for a linear color gradient."""
        self.start_color = start_color
        self.end_color = end_color

    def generate(self, count: int) -> List[str]:
        """Generate a list of hex colors for the given number of steps."""
        if count <= 1:
            return [self._to_hex(self.start_color)]
        colors: List[str] = []
        step_red = (self.end_color[0] - self.start_color[0]) / (count - 1)
        step_green = (self.end_color[1] - self.start_color[1]) / (count - 1)
        step_blue = (self.end_color[2] - self.start_color[2]) / (count - 1)
        for index in range(count):
            red_value = round(self.start_color[0] + step_red * index)
            green_value = round(self.start_color[1] + step_green * index)
            blue_value = round(self.start_color[2] + step_blue * index)
            colors.append(self._to_hex((red_value, green_value, blue_value)))
        return colors

    def _to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert an RGB tuple into a hex color string."""
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"


class TreeVisualizer:
    def __init__(self) -> None:
        """Initialize the visualization graph."""
        self.graph = nx.DiGraph()

    def _add_edges(
        self,
        node: Optional[Node],
        positions: Dict[str, Tuple[float, float]],
        horizontal_pos: float = 0.0,
        vertical_pos: float = 0.0,
        layer_number: int = 1,
    ) -> None:
        """Add nodes and edges to the graph for drawing."""
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

    def draw(self, root: Node, title: str = "") -> None:
        """Draw the current tree state with node colors."""
        self.graph.clear()
        positions: Dict[str, Tuple[float, float]] = {root.node_id: (0.0, 0.0)}
        self._add_edges(root, positions)
        colors = [node[1]["color"] for node in self.graph.nodes(data=True)]
        labels = {node[0]: node[1]["label"] for node in self.graph.nodes(data=True)}
        plt.clf()
        if title:
            plt.title(title)
        nx.draw(self.graph, pos=positions, labels=labels, arrows=False, node_size=2500, node_color=colors)
        plt.pause(0.7)


class TreeTraversal:
    def __init__(self, root: Node) -> None:
        """Store the root node for traversals."""
        self.root = root

    def dfs(self) -> List[Node]:
        """Perform an iterative depth-first traversal using a stack."""
        order: List[Node] = []
        stack: List[Node] = [self.root]
        while stack:
            current_node = stack.pop()
            order.append(current_node)
            if current_node.right:
                stack.append(current_node.right)
            if current_node.left:
                stack.append(current_node.left)
        return order

    def bfs(self) -> List[Node]:
        """Perform an iterative breadth-first traversal using a queue."""
        order: List[Node] = []
        queue: Deque[Node] = deque([self.root])
        while queue:
            current_node = queue.popleft()
            order.append(current_node)
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
        return order


class TraversalDemo:
    def __init__(self) -> None:
        """Set up the demo tree and visualization helpers."""
        self.values = [0, 4, 1, 5, 10, 3]
        builder = TreeBuilder(self.values)
        self.root = builder.build()
        self.visualizer = TreeVisualizer()
        self.palette = ColorPalette(start_color=(50, 0, 100), end_color=(150, 255, 255))

    def animate(self, order: Iterable[Node], title: str) -> None:
        """Animate traversal by updating node colors in order."""
        nodes = list(order)
        colors = self.palette.generate(len(nodes))
        plt.figure(figsize=(8, 5))
        for node, color in zip(nodes, colors):
            node.color = color
            self.visualizer.draw(self.root, title=title)
        plt.show()

    def run(self) -> None:
        """Run DFS and BFS visualizations sequentially."""
        traversal = TreeTraversal(self.root)
        self.animate(traversal.dfs(), "DFS")
        self.root = TreeBuilder(self.values).build()
        self.visualizer = TreeVisualizer()
        traversal = TreeTraversal(self.root)
        self.animate(traversal.bfs(), "BFS")


if __name__ == "__main__":
    demo = TraversalDemo()
    demo.run()
