    def get_hatch_path(self, density=6.0):
        """
        Returns a Path for the current hatch.
        """
        hatch = self.get_hatch()
        if hatch is None:
            return None
        return Path.hatch(hatch, density)
