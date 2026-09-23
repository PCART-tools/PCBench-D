    @martist.allow_rasterization
    def draw(self, renderer, *args, **kwargs):
        # if not visible, declare victory and return
        if not self.get_visible():
            self.stale = False
            return

        # for empty images, there is nothing to draw!
        if self.get_array().size == 0:
            self.stale = False
            return

        # actually render the image.
        gc = renderer.new_gc()
        self._set_gc_clip(gc)
        gc.set_alpha(self._get_scalar_alpha())
        gc.set_url(self.get_url())
        gc.set_gid(self.get_gid())

        if (self._check_unsampled_image(renderer) and
                self.get_transform().is_affine):
            self._draw_unsampled_image(renderer, gc)
        else:
            im, l, b, trans = self.make_image(
                renderer, renderer.get_image_magnification())
            if im is not None:
                renderer.draw_image(gc, l, b, im)
        gc.restore()
        self.stale = False
