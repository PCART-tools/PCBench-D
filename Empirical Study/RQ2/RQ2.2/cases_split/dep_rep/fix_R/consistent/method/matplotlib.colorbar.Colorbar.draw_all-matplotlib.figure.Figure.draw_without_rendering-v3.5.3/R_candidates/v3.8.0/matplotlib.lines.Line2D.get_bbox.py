    def get_bbox(self):
        """Get the bounding box of this line."""
        bbox = Bbox([[0, 0], [0, 0]])
        bbox.update_from_data_xy(self.get_xydata())
        return bbox
