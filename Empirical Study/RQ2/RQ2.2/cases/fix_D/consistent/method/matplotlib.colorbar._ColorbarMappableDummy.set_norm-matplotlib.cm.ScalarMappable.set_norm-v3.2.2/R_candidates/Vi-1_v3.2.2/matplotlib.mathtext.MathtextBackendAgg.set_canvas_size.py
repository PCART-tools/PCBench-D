    def set_canvas_size(self, w, h, d):
        MathtextBackend.set_canvas_size(self, w, h, d)
        if self.mode != 'bbox':
            self.image = FT2Image(np.ceil(w), np.ceil(h + max(d, 0)))
