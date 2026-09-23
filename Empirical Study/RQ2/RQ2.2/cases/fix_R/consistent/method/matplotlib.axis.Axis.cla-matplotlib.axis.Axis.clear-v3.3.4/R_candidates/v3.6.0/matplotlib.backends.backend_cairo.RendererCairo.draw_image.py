    def draw_image(self, gc, x, y, im):
        im = cbook._unmultiplied_rgba8888_to_premultiplied_argb32(im[::-1])
        surface = cairo.ImageSurface.create_for_data(
            im.ravel().data, cairo.FORMAT_ARGB32,
            im.shape[1], im.shape[0], im.shape[1] * 4)
        ctx = gc.ctx
        y = self.height - y - im.shape[0]

        ctx.save()
        ctx.set_source_surface(surface, float(x), float(y))
        ctx.paint()
        ctx.restore()
