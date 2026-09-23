    def hatchPattern(self, hatch_style):
        # The colors may come in as numpy arrays, which aren't hashable
        if hatch_style is not None:
            edge, face, hatch = hatch_style
            if edge is not None:
                edge = tuple(edge)
            if face is not None:
                face = tuple(face)
            hatch_style = (edge, face, hatch)

        pattern = self.hatchPatterns.get(hatch_style, None)
        if pattern is not None:
            return pattern

        name = next(self._hatch_pattern_seq)
        self.hatchPatterns[hatch_style] = name
        return name
