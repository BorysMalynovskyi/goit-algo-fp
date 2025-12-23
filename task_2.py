import math
import turtle


class PythagorasTree:
    def __init__(self, depth: int, trunk_length: float = 80.0, angle_degrees: float = 45.0) -> None:
        """Initialize the tree parameters and set up the turtle screen."""
        self.depth = depth
        self.trunk_length = trunk_length
        self.angle_degrees = angle_degrees
        self.canvas = turtle.Screen()
        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)

    def draw(self) -> None:
        """Draw the Pythagoras tree using recursion."""
        self.pen.left(90)
        self.pen.up()
        self.pen.backward(self.trunk_length * 0.6)
        self.pen.down()
        self._draw_branch(self.trunk_length, self.depth)
        self.canvas.mainloop()

    def _draw_branch(self, branch_length: float, remaining_depth: int) -> None:
        """Recursively draw branches with decreasing length."""
        if remaining_depth == 0:
            return
        self.pen.forward(branch_length)
        self.pen.left(self.angle_degrees)
        self._draw_branch(branch_length * math.sqrt(0.5), remaining_depth - 1)
        self.pen.right(2 * self.angle_degrees)
        self._draw_branch(branch_length * math.sqrt(0.5), remaining_depth - 1)
        self.pen.left(self.angle_degrees)
        self.pen.backward(branch_length)


class DepthInput:
    def __init__(self, prompt: str = "Enter recursion depth: ") -> None:
        """Store the prompt used to read recursion depth from the user."""
        self.prompt = prompt

    def read_depth(self) -> int:
        """Read and validate recursion depth from user input."""
        while True:
            raw_value = input(self.prompt).strip()
            if raw_value.isdigit():
                depth_value = int(raw_value)
                if depth_value >= 0:
                    return depth_value
            print("Please enter a non-negative integer.")


if __name__ == "__main__":
    depth_reader = DepthInput()
    recursion_depth = depth_reader.read_depth()
    tree = PythagorasTree(depth=recursion_depth)
    tree.draw()
