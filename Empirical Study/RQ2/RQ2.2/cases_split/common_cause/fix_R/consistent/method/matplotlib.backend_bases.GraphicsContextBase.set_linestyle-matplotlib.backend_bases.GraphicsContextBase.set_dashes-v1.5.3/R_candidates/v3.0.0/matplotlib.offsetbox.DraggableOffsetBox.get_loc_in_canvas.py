    def get_loc_in_canvas(self):

        offsetbox = self.offsetbox
        renderer = offsetbox.figure._cachedRenderer
        w, h, xd, yd = offsetbox.get_extent(renderer)
        ox, oy = offsetbox._offset
        loc_in_canvas = (ox - xd, oy - yd)

        return loc_in_canvas
