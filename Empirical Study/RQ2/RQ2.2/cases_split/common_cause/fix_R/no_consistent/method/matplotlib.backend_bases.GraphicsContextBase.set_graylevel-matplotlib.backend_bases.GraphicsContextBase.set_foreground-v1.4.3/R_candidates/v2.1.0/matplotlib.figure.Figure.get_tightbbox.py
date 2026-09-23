    def get_tightbbox(self, renderer):
        """
        Return a (tight) bounding box of the figure in inches.

        It only accounts axes title, axis labels, and axis
        ticklabels. Needs improvement.
        """

        bb = []
        for ax in self.axes:
            if ax.get_visible():
                bb.append(ax.get_tightbbox(renderer))

        if len(bb) == 0:
            return self.bbox_inches

        _bbox = Bbox.union([b for b in bb if b.width != 0 or b.height != 0])

        bbox_inches = TransformedBbox(_bbox,
                                      Affine2D().scale(1. / self.dpi))

        return bbox_inches
