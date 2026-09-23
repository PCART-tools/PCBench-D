    def get_visible_children(self):
        r"""Return a list of the visible child `.Artist`\s."""
        return [c for c in self._children if c.get_visible()]
