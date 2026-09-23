    def _get_anchored_bbox(self, loc, bbox, parentbbox, renderer):
        """
        Place the *bbox* inside the *parentbbox* according to a given
        location code. Return the (x, y) coordinate of the bbox.

        Parameters
        ----------
        loc : int
            A location code in range(1, 11). This corresponds to the possible
            values for ``self._loc``, excluding "best".
        bbox : `~matplotlib.transforms.Bbox`
            bbox to be placed, in display coordinates.
        parentbbox : `~matplotlib.transforms.Bbox`
            A parent box which will contain the bbox, in display coordinates.

        """
        assert loc in range(1, 11)  # called only internally

        BEST, UR, UL, LL, LR, R, CL, CR, LC, UC, C = range(11)

        anchor_coefs = {UR: "NE",
                        UL: "NW",
                        LL: "SW",
                        LR: "SE",
                        R: "E",
                        CL: "W",
                        CR: "E",
                        LC: "S",
                        UC: "N",
                        C: "C"}

        c = anchor_coefs[loc]

        fontsize = renderer.points_to_pixels(self._fontsize)
        container = parentbbox.padded(-self.borderaxespad * fontsize)
        anchored_box = bbox.anchored(c, container=container)
        return anchored_box.x0, anchored_box.y0
