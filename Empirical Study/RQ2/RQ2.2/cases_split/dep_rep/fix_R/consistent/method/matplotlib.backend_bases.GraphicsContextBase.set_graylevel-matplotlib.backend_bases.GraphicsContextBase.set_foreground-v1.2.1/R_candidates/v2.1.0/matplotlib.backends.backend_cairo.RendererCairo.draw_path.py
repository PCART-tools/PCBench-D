    def draw_path(self, gc, path, transform, rgbFace=None):
        ctx = gc.ctx

        # We'll clip the path to the actual rendering extents
        # if the path isn't filled.
        if rgbFace is None and gc.get_hatch() is None:
            clip = ctx.clip_extents()
        else:
            clip = None

        transform = (transform
                     + Affine2D().scale(1.0, -1.0).translate(0, self.height))

        ctx.new_path()
        self.convert_path(ctx, path, transform, clip)

        self._fill_and_stroke(
            ctx, rgbFace, gc.get_alpha(), gc.get_forced_alpha())
