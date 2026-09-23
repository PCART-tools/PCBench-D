    def _draw_unsampled_image(self, renderer, gc):
        """
        Draw unsampled image. The renderer should support a draw_image method
        with scale parameter.
        """
        im, l, b, trans = self.make_image(renderer, unsampled=True)

        if im is None:
            return

        trans = Affine2D().scale(im.shape[1], im.shape[0]) + trans

        renderer.draw_image(gc, l, b, im, trans)
