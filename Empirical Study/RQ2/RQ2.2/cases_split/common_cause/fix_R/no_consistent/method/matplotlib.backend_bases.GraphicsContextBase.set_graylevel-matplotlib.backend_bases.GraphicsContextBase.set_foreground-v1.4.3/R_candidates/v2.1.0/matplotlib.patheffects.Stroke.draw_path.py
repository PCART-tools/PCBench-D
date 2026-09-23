    def draw_path(self, renderer, gc, tpath, affine, rgbFace):
        """
        draw the path with updated gc.
        """
        # Do not modify the input! Use copy instead.

        gc0 = renderer.new_gc()
        gc0.copy_properties(gc)

        gc0 = self._update_gc(gc0, self._gc)
        trans = self._offset_transform(renderer, affine)
        renderer.draw_path(gc0, tpath, trans, rgbFace)
        gc0.restore()
