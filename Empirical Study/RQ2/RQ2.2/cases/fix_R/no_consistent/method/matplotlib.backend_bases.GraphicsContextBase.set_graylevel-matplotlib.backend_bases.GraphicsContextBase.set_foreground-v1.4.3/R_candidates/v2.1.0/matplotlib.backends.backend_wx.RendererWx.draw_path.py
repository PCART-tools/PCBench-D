    def draw_path(self, gc, path, transform, rgbFace=None):
        gc.select()
        self.handle_clip_rectangle(gc)
        gfx_ctx = gc.gfx_ctx
        transform = transform + \
            Affine2D().scale(1.0, -1.0).translate(0.0, self.height)
        wxpath = self.convert_path(gfx_ctx, path, transform)
        if rgbFace is not None:
            gfx_ctx.SetBrush(wx.Brush(gc.get_wxcolour(rgbFace)))
            gfx_ctx.DrawPath(wxpath)
        else:
            gfx_ctx.StrokePath(wxpath)
        gc.unselect()
