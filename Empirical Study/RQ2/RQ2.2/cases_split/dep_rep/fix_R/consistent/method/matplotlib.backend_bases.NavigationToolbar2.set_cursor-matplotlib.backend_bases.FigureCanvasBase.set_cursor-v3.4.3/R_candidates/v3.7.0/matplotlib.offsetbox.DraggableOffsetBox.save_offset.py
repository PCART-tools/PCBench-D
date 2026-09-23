    def save_offset(self):
        offsetbox = self.offsetbox
        renderer = offsetbox.figure._get_renderer()
        offset = offsetbox.get_offset(offsetbox.get_bbox(renderer), renderer)
        self.offsetbox_x, self.offsetbox_y = offset
        self.offsetbox.set_offset(offset)
