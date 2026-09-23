    def get_path(self):
        """Return a `.Path` for the `.visible_edges`."""
        codes = [Path.MOVETO]
        codes.extend(
            Path.LINETO if edge in self._visible_edges else Path.MOVETO
            for edge in self._edges)
        if Path.MOVETO not in codes[1:]:  # All sides are visible
            codes[-1] = Path.CLOSEPOLY
        return Path(
            [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]],
            codes,
            readonly=True
            )
