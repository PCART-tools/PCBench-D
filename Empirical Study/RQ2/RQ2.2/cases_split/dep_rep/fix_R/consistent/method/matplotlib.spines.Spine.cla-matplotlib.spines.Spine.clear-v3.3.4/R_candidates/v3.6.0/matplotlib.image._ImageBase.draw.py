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
        if (renderer.option_scale_image()  # Renderer supports transform kwarg.
                and self._check_unsampled_image()
                and self.get_transform().is_affine):
            im, l, b, trans = self.make_image(renderer, unsampled=True)
            if im is not None:
                trans = Affine2D().scale(im.shape[1], im.shape[0]) + trans
                renderer.draw_image(gc, l, b, im, trans)
        else:
            im, l, b, trans = self.make_image(
                renderer, renderer.get_image_magnification())
            if im is not None:
                renderer.draw_image(gc, l, b, im)
        gc.restore()
        self.stale = False
