    def make_image(self, renderer, magnification=1.0, unsampled=False):
        # docstring inherited
        trans = self.get_transform()
        # image is created in the canvas coordinate.
        x1, x2, y1, y2 = self.get_extent()
        bbox = Bbox(np.array([[x1, y1], [x2, y2]]))
        transformed_bbox = TransformedBbox(bbox, trans)
        clip = ((self.get_clip_box() or self.axes.bbox) if self.get_clip_on()
                else self.get_figure(root=True).bbox)
        return self._make_image(self._A, bbox, transformed_bbox, clip,
                                magnification, unsampled=unsampled)
