    def get_datalim(self, transData):
        return (self.get_transform() - transData).transform_bbox(self._bbox)
