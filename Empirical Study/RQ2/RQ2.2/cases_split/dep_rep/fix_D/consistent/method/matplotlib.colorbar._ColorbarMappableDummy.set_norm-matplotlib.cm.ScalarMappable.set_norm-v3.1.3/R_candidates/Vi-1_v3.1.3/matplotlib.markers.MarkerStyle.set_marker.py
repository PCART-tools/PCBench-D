    def set_marker(self, marker):
        if (isinstance(marker, np.ndarray) and marker.ndim == 2 and
                marker.shape[1] == 2):
            self._marker_function = self._set_vertices
        elif isinstance(marker, str) and cbook.is_math_text(marker):
            self._marker_function = self._set_mathtext_path
        elif isinstance(marker, Path):
            self._marker_function = self._set_path_marker
        elif (isinstance(marker, Sized) and len(marker) in (2, 3) and
                marker[1] in (0, 1, 2, 3)):
            self._marker_function = self._set_tuple_marker
        elif (not isinstance(marker, (np.ndarray, list)) and
              marker in self.markers):
            self._marker_function = getattr(
                self, '_set_' + self.markers[marker])
        else:
            try:
                Path(marker)
                self._marker_function = self._set_vertices
            except ValueError:
                raise ValueError('Unrecognized marker style {!r}'
                                 .format(marker))

        self._marker = marker
        self._recache()
