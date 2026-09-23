    def get_loc_in_canvas(self):
        offsetbox = self.offsetbox
        renderer = offsetbox.get_figure(root=True)._get_renderer()
        bbox = offsetbox.get_bbox(renderer)
        ox, oy = offsetbox._offset
        loc_in_canvas = (ox + bbox.x0, oy + bbox.y0)
        return loc_in_canvas
