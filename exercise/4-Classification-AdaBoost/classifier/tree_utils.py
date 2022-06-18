from typing import List


class Node:
    """Node of a tree. Can consist of multiple branches,
    if no branches exist then node is not an internal node but a leaf node."""

    def __init__(self, label: str, branches: List = None) -> None:
        self.label = label
        # Our decision trees may support multiway splits.
        # Therefore, we store our branches or children as a list.
        # Should be of type List[Branch], but in this JupyterNotebook cell
        # it is not possible to reference the object Branch before it is defined.
        # We refrained form creating a package for these two objects.
        self.branches = branches

    def __repr__(self) -> str:
        """Special method to return a string containing a printable
        representation of this custom object. This representation can
        be used to create this very same object when the value is passed
        to eval()."""
        return "Node(%r, %r)" % (self.label, self.branches)


class Branch:
    """Branch of a tree containing a label and a (internal/leaf) node."""

    def __init__(self, label: str, node: Node = None) -> None:
        self.label = label
        # Actual child of a tree Node.
        self.node = node

    def __repr__(self) -> str:
        """Special method to return a string containing a printable
        representation of this custom object. This representation can
        be used to create this very same object when the value is passed
        to eval()."""
        return "Branch(%r, %r)" % (self.label, self.node)
