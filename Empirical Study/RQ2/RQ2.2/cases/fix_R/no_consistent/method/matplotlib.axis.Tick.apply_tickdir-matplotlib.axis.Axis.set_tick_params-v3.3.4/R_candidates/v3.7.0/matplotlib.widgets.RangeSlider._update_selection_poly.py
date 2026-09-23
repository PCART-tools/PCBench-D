    def _update_selection_poly(self, vmin, vmax):
        """
        Update the vertices of the *self.poly* slider in-place
        to cover the data range *vmin*, *vmax*.
        """
        # The vertices are positioned
        #  1 ------ 2
        #  |        |
        # 0, 4 ---- 3
        verts = self.poly.xy
        if self.orientation == "vertical":
            verts[0] = verts[4] = .25, vmin
            verts[1] = .25, vmax
            verts[2] = .75, vmax
            verts[3] = .75, vmin
        else:
            verts[0] = verts[4] = vmin, .25
            verts[1] = vmin, .75
            verts[2] = vmax, .75
            verts[3] = vmax, .25
