class Node(tuple):
    """A Discrimination Net node."""

    __slots__ = ()

    def __new__(cls, edges=None, patterns=None):
        edges = edges if edges else {}
        patterns = patterns if patterns else []
        return tuple.__new__(cls, (edges, patterns))

    @property
    def edges(self):
        """A dictionary, where the keys are edges, and the values are nodes"""
        return self[0]

    @property
    def patterns(self):
        """A list of all patterns that currently match at this node"""
        return self[1]
