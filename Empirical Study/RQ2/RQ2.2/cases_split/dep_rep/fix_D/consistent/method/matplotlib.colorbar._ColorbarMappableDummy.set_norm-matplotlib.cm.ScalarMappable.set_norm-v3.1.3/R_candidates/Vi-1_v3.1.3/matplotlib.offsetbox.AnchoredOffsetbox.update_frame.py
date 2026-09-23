    def update_frame(self, bbox, fontsize=None):
        self.patch.set_bounds(bbox.x0, bbox.y0,
                              bbox.width, bbox.height)

        if fontsize:
            self.patch.set_mutation_scale(fontsize)
