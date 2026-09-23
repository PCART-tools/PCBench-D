    def draw_image(self, gc, x, y, im):
        bbox = gc.get_clip_rectangle()
        if bbox is not None:
            l, b, w, h = bbox.bounds
        else:
            l = 0
            b = 0
            w = self.width
            h = self.height
        rows, cols = im.shape[:2]
        bitmap = wx.Bitmap.FromBufferRGBA(cols, rows, im.tobytes())
        gc.select()
        gc.gfx_ctx.DrawBitmap(bitmap, int(l), int(self.height - b),
                              int(w), int(-h))
        gc.unselect()
