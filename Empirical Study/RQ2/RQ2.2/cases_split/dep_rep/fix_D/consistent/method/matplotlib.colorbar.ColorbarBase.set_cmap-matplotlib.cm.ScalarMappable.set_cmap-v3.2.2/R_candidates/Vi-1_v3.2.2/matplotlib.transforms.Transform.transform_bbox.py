    def transform_bbox(self, bbox):
        """
        Transform the given bounding box.

        Note, for smarter transforms including caching (a common
        requirement for matplotlib figures), see :class:`TransformedBbox`.
        """
        return Bbox(self.transform(bbox.get_points()))
