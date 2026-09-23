class Node:
    """A node in the TeX box model."""

    def __init__(self):
        self.size = 0

    def __repr__(self):
        return self.__class__.__name__

    def get_kerning(self, next):
        return 0.0

    def shrink(self):
        """
        Shrinks one level smaller.  There are only three levels of
        sizes, after which things will no longer get smaller.
        """
        self.size += 1

    def grow(self):
        """
        Grows one level larger.  There is no limit to how big
        something can get.
        """
        self.size -= 1

    def render(self, x, y):
        pass
