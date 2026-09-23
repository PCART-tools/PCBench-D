    def draw(self, renderer):
        if not self.get_visible():
            return

        # FIXME: dpi_cor is for the dpi-dependency of the linewidth.  There
        # could be room for improvement.  Maybe _get_path_in_displaycoord could
        # take a renderer argument, but get_path should be adapted too.
        self._dpi_cor = renderer.points_to_pixels(1.)
        path, fillable = self._get_path_in_displaycoord()

        if not np.iterable(fillable):
            path = [path]
            fillable = [fillable]

        affine = transforms.IdentityTransform()

        self._draw_paths_with_artist_properties(
            renderer,
            [(p, affine, self._facecolor if f and self._facecolor[3] else None)
             for p, f in zip(path, fillable)])
