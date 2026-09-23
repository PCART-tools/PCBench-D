    def get_tight_layout(self):
        """Return whether `.tight_layout` is called when drawing."""
        return isinstance(self.get_layout_engine(), TightLayoutEngine)
