    def __call__(self, ax, renderer):
        bbox_parent = self.parent.get_position(original=False)
        trans = BboxTransformTo(bbox_parent)
        bbox_inset = Bbox.from_bounds(*self.lbwh)
        bb = TransformedBbox(bbox_inset, trans)
        return bb
