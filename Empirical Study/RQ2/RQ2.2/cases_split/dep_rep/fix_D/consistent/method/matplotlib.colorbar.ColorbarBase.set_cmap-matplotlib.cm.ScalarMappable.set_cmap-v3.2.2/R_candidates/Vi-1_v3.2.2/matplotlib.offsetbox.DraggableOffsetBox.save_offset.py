    def save_offset(self):
        offsetbox = self.offsetbox
        renderer = offsetbox.figure._cachedRenderer
        w, h, xd, yd = offsetbox.get_extent(renderer)
        offset = offsetbox.get_offset(w, h, xd, yd, renderer)
        self.offsetbox_x, self.offsetbox_y = offset
        self.offsetbox.set_offset(offset)
