    def _revalidate_path(self):
        """
        update the path if necessary.

        The path for the text is initially create with the font size
        of FONT_SCALE, and this path is rescaled to other size when
        necessary.

        """
        if self._invalid or self._cached_vertices is None:
            tr = Affine2D().scale(
                    self._size / text_to_path.FONT_SCALE,
                    self._size / text_to_path.FONT_SCALE).translate(*self._xy)
            self._cached_vertices = tr.transform(self._vertices)
            self._invalid = False
