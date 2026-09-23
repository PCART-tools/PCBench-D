    def set_canvas_size(self, w, h, d):
        MathtextBackend.set_canvas_size(self, w, h, d)
        if self.mode != 'bbox':
            self.image = FT2Image(ceil(w), ceil(h + max(d, 0)))
