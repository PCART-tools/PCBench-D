    def contains(self, x, y):
        """
        Return whether ``(x, y)`` is in the bounding box or on its edge.
        """
        return self.containsx(x) and self.containsy(y)
