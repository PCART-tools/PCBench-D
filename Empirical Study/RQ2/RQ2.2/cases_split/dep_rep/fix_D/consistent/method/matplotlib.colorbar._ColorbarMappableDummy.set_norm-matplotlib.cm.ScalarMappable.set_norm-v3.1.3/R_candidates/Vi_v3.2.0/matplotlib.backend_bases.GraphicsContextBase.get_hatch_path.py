    def get_hatch_path(self, density=6.0):
        """Return a `Path` for the current hatch."""
        hatch = self.get_hatch()
        if hatch is None:
            return None
        return Path.hatch(hatch, density)
