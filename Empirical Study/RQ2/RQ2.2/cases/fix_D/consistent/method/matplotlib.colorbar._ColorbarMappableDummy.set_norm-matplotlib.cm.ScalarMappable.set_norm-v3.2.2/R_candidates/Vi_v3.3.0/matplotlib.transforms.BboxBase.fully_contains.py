    def fully_contains(self, x, y):
        """
        Return whether ``x, y`` is in the bounding box, but not on its edge.
        """
        return self.fully_containsx(x) and self.fully_containsy(y)
