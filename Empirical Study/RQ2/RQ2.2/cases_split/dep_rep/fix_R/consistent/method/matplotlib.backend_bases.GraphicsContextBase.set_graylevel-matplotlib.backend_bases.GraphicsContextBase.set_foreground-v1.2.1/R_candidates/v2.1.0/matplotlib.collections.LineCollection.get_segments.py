    def get_segments(self):
        segments = []

        for path in self._paths:
            vertices = [vertex for vertex, _ in path.iter_segments()]
            vertices = np.asarray(vertices)
            segments.append(vertices)

        return segments
