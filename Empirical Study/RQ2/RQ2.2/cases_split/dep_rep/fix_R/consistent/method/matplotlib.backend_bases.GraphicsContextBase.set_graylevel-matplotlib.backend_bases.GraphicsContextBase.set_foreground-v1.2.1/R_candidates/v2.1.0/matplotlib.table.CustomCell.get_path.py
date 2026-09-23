    def get_path(self):
        'Return a path where the edges specificed by _visible_edges are drawn'

        codes = [Path.MOVETO]

        for edge in self._edges:
            if edge in self._visible_edges:
                codes.append(Path.LINETO)
            else:
                codes.append(Path.MOVETO)

        if Path.MOVETO not in codes[1:]:  # All sides are visible
            codes[-1] = Path.CLOSEPOLY

        return Path(
            [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0], [0.0, 0.0]],
            codes,
            readonly=True
            )
