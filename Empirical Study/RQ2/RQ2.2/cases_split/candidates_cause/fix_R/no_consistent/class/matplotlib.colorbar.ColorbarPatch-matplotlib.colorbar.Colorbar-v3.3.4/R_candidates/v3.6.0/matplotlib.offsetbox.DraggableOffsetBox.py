class DraggableOffsetBox(DraggableBase):
    def __init__(self, ref_artist, offsetbox, use_blit=False):
        super().__init__(ref_artist, use_blit=use_blit)
        self.offsetbox = offsetbox

    def save_offset(self):
        offsetbox = self.offsetbox
        renderer = offsetbox.figure._get_renderer()
        w, h, xd, yd = offsetbox.get_extent(renderer)
        offset = offsetbox.get_offset(w, h, xd, yd, renderer)
        self.offsetbox_x, self.offsetbox_y = offset
        self.offsetbox.set_offset(offset)

    def update_offset(self, dx, dy):
        loc_in_canvas = self.offsetbox_x + dx, self.offsetbox_y + dy
        self.offsetbox.set_offset(loc_in_canvas)

    def get_loc_in_canvas(self):
        offsetbox = self.offsetbox
        renderer = offsetbox.figure._get_renderer()
        w, h, xd, yd = offsetbox.get_extent(renderer)
        ox, oy = offsetbox._offset
        loc_in_canvas = (ox - xd, oy - yd)
        return loc_in_canvas
