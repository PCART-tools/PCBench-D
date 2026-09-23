    def _repr_html_(self):
        """Generate an HTML representation of the MultivarColormap."""
        return ''.join([c._repr_html_() for c in self._colormaps])
