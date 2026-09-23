    def set_parent(self, parent):
        """Replace the parent of this with the new parent."""
        self.parent = parent
        self.parent_constrain()
