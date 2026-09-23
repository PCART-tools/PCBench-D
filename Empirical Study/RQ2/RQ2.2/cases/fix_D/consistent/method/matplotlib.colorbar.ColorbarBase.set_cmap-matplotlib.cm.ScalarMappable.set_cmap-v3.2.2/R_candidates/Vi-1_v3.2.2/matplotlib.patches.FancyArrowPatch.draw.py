    def draw(self, renderer):
        if not self.get_visible():
            return

        with self._bind_draw_path_function(renderer) as draw_path:

            # FIXME : dpi_cor is for the dpi-dependency of the linewidth. There
            # could be room for improvement.
            self.set_dpi_cor(renderer.points_to_pixels(1.))
            path, fillable = self.get_path_in_displaycoord()

            if not np.iterable(fillable):
                path = [path]
                fillable = [fillable]

            affine = transforms.IdentityTransform()

            for p, f in zip(path, fillable):
                draw_path(
                    p, affine,
                    self._facecolor if f and self._facecolor[3] else None)
