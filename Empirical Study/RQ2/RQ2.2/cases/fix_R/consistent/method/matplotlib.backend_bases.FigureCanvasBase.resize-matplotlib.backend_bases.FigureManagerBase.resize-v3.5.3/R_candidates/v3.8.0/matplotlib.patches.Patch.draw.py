    @artist.allow_rasterization
    def draw(self, renderer):
        # docstring inherited
        if not self.get_visible():
            return
        path = self.get_path()
        transform = self.get_transform()
        tpath = transform.transform_path_non_affine(path)
        affine = transform.get_affine()
        self._draw_paths_with_artist_properties(
            renderer,
            [(tpath, affine,
              # Work around a bug in the PDF and SVG renderers, which
              # do not draw the hatches if the facecolor is fully
              # transparent, but do if it is None.
              self._facecolor if self._facecolor[3] else None)])
