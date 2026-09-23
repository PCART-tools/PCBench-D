    def __iter__(self):
        boundarystream = InterBoundaryIter(self._stream, self._separator)
        for sub_stream in boundarystream:
            # Iterate over each part
            yield parse_boundary_stream(sub_stream, 1024)
