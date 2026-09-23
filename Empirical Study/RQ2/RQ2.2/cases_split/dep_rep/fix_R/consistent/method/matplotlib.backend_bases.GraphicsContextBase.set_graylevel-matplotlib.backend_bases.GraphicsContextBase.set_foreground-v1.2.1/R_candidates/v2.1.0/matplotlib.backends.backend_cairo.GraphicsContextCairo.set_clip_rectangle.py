    def set_clip_rectangle(self, rectangle):
        if not rectangle:
            return
        x, y, w, h = rectangle.bounds
        # pixel-aligned clip-regions are faster
        x,y,w,h = np.round(x), np.round(y), np.round(w), np.round(h)
        ctx = self.ctx
        ctx.new_path()
        ctx.rectangle(x, self.renderer.height - h - y, w, h)
        ctx.clip()
