from dataclasses import dataclass
from typing import Iterable, Optional, Tuple


@dataclass
class Node:
    value: int
    next_node: Optional["Node"] = None


class LinkedList:
    def __init__(self, values: Optional[Iterable[int]] = None) -> None:
        """Initialize a singly linked list from an optional iterable of values."""
        self.head: Optional[Node] = None
        if values is not None:
            for item in values:
                self.append(item)

    def append(self, value: int) -> None:
        """Append a value to the end of the list."""
        new_node = Node(value=value)
        if self.head is None:
            self.head = new_node
            return
        current_node = self.head
        while current_node.next_node is not None:
            current_node = current_node.next_node
        current_node.next_node = new_node

    def to_list(self) -> list[int]:
        """Return a Python list representation of the linked list."""
        result: list[int] = []
        current_node = self.head
        while current_node is not None:
            result.append(current_node.value)
            current_node = current_node.next_node
        return result

    def reverse(self) -> None:
        """Reverse the linked list in place by re-linking nodes."""
        previous_node: Optional[Node] = None
        current_node = self.head
        while current_node is not None:
            next_node = current_node.next_node
            current_node.next_node = previous_node
            previous_node = current_node
            current_node = next_node
        self.head = previous_node

    def sort(self) -> None:
        """Sort the linked list in ascending order using merge sort."""
        self.head = self._merge_sort(self.head)

    def merge_sorted(self, other: "LinkedList") -> "LinkedList":
        """Merge two sorted linked lists into a single sorted list."""
        merged_head = self._merge(self.head, other.head)
        merged_list = LinkedList()
        merged_list.head = merged_head
        return merged_list

    def _merge_sort(self, head: Optional[Node]) -> Optional[Node]:
        """Recursively split and merge nodes to perform merge sort."""
        if head is None or head.next_node is None:
            return head
        left_half, right_half = self._split(head)
        sorted_left = self._merge_sort(left_half)
        sorted_right = self._merge_sort(right_half)
        return self._merge(sorted_left, sorted_right)

    def _split(self, head: Node) -> Tuple[Optional[Node], Optional[Node]]:
        """Split the list into two halves and return their heads."""
        slow_node = head
        fast_node = head.next_node
        while fast_node is not None and fast_node.next_node is not None:
            if slow_node.next_node is None:
                break
            slow_node = slow_node.next_node
            fast_node = fast_node.next_node.next_node
        middle_node = slow_node.next_node
        slow_node.next_node = None
        return head, middle_node

    def _merge(self, left_head: Optional[Node], right_head: Optional[Node]) -> Optional[Node]:
        """Merge two sorted linked lists and return the merged head."""
        dummy_head = Node(value=0)
        tail_node = dummy_head
        left_node = left_head
        right_node = right_head
        while left_node is not None and right_node is not None:
            if left_node.value <= right_node.value:
                tail_node.next_node = left_node
                left_node = left_node.next_node
            else:
                tail_node.next_node = right_node
                right_node = right_node.next_node
            tail_node = tail_node.next_node
        tail_node.next_node = left_node if left_node is not None else right_node
        return dummy_head.next_node


def build_demo_lists() -> tuple[LinkedList, LinkedList]:
    """Create demo linked lists for quick manual verification."""
    first_list = LinkedList([4, 2, 5, 1, 3])
    second_list = LinkedList([6, 7, 8])
    return first_list, second_list


if __name__ == "__main__":
    list_a, list_b = build_demo_lists()
    list_a.reverse()
    print("Reversed:", list_a.to_list())

    list_a.sort()
    print("Sorted:", list_a.to_list())

    list_b.sort()
    merged = list_a.merge_sorted(list_b)
    print("Merged:", merged.to_list())
