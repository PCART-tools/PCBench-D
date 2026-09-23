class Node:
    """A node in the TeX box model."""

    def __init__(self):
        self.size = 0

    def __repr__(self):
        return type(self).__name__

    def get_kerning(self, next):
        return 0.0

    def shrink(self):
        """
        Shrinks one level smaller.  There are only three levels of
        sizes, after which things will no longer get smaller.
        """
        self.size += 1

    def render(self, output, x, y):
        """Render this node."""
