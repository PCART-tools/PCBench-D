    def transform_bbox(self, bbox):
        """
        Transform the given bounding box.

        For smarter transforms including caching (a common requirement in
        Matplotlib), see `TransformedBbox`.
        """
        return Bbox(self.transform(bbox.get_points()))
