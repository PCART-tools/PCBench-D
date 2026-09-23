    def scaled(self):
        """Return whether *vmin* and *vmax* are both set."""
        return self.vmin is not None and self.vmax is not None
