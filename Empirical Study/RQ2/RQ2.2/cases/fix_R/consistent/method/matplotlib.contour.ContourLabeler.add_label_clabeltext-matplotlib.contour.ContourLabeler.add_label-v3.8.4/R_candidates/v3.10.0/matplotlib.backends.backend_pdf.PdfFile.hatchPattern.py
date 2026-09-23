    def hatchPattern(self, hatch_style):
        # The colors may come in as numpy arrays, which aren't hashable
        edge, face, hatch, lw = hatch_style
        if edge is not None:
            edge = tuple(edge)
        if face is not None:
            face = tuple(face)
        hatch_style = (edge, face, hatch, lw)

        pattern = self._hatch_patterns.get(hatch_style, None)
        if pattern is not None:
            return pattern

        name = next(self._hatch_pattern_seq)
        self._hatch_patterns[hatch_style] = name
        return name
