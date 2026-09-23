    @artist.allow_rasterization
    def draw(self, renderer):
        """Draw to the given *renderer*."""
        if not self.get_visible():
            return

        # Patch has traditionally ignored the dashoffset.
        with cbook._setattr_cm(self, _dashoffset=0), \
                self._bind_draw_path_function(renderer) as draw_path:
            path = self.get_path()
            transform = self.get_transform()
            tpath = transform.transform_path_non_affine(path)
            affine = transform.get_affine()
            draw_path(tpath, affine,
                      # Work around a bug in the PDF and SVG renderers, which
                      # do not draw the hatches if the facecolor is fully
                      # transparent, but do if it is None.
                      self._facecolor if self._facecolor[3] else None)
