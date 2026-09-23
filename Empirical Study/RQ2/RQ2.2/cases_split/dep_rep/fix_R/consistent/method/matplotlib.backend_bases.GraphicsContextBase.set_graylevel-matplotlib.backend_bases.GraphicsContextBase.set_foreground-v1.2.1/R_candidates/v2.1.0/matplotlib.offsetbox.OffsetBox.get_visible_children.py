    def get_visible_children(self):
        """
        Return a list of visible artists it contains.
        """
        return [c for c in self._children if c.get_visible()]
