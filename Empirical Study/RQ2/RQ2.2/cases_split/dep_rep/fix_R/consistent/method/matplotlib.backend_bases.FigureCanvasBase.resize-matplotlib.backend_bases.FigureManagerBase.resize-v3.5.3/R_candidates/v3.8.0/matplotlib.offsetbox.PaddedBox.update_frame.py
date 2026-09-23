    def update_frame(self, bbox, fontsize=None):
        self.patch.set_bounds(bbox.bounds)
        if fontsize:
            self.patch.set_mutation_scale(fontsize)
        self.stale = True
