    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        """
        Overrides the standard draw_path to add the shadow offset and
        necessary color changes for the shadow.

        """
        # IMPORTANT: Do not modify the input - we copy everything instead.
        affine0 = self._offset_transform(renderer, affine)
        gc0 = renderer.new_gc()
        gc0.copy_properties(gc)

        if self._shadow_color is None:
            r, g, b = (gc0.get_foreground() or (1., 1., 1.))[:3]
            # Scale the colors by a factor to improve the shadow effect.
            shadow_rgbFace = (r * self._rho, g * self._rho, b * self._rho)
        else:
            shadow_rgbFace = self._shadow_color

        fill_color = None

        gc0.set_foreground(shadow_rgbFace)
        gc0.set_alpha(self._alpha)

        gc0 = self._update_gc(gc0, self._gc)
        renderer.draw_path(gc0, tpath, affine0, fill_color)
        gc0.restore()
