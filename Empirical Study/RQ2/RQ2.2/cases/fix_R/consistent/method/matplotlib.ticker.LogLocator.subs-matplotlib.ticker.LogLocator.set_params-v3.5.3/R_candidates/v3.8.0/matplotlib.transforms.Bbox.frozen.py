    def frozen(self):
        # docstring inherited
        frozen_bbox = super().frozen()
        frozen_bbox._minpos = self.minpos.copy()
        return frozen_bbox
