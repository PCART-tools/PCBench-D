    def _update_bbox_to_anchor(self, loc_in_canvas):

        tr = self.legend.axes.transAxes
        loc_in_bbox = tr.transform_point(loc_in_canvas)

        self.legend.set_bbox_to_anchor(loc_in_bbox)
