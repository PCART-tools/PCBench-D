    def get_datalim(self, transData):
        trans = self.get_transform()
        transOffset = self.get_offset_transform()
        full_transform = (trans - transData) + (transOffset - transData)
        XY = full_transform.transform(self.XY)
        bbox = transforms.Bbox.null()
        bbox.update_from_data_xy(XY, ignore=True)
        return bbox
