    def _update_position_xybox(self, renderer, xy_pixel):
        """
        Update the pixel positions of the annotation text and the arrow patch.
        """

        x, y = self.xybox
        if isinstance(self.boxcoords, tuple):
            xcoord, ycoord = self.boxcoords
            x1, y1 = self._get_xy(renderer, x, y, xcoord)
            x2, y2 = self._get_xy(renderer, x, y, ycoord)
            ox0, oy0 = x1, y2
        else:
            ox0, oy0 = self._get_xy(renderer, x, y, self.boxcoords)

        w, h, xd, yd = self.offsetbox.get_extent(renderer)

        _fw, _fh = self._box_alignment
        self.offsetbox.set_offset((ox0 - _fw * w + xd, oy0 - _fh * h + yd))

        # update patch position
        bbox = self.offsetbox.get_window_extent(renderer)
        #self.offsetbox.set_offset((ox0-_fw*w, oy0-_fh*h))
        self.patch.set_bounds(bbox.x0, bbox.y0,
                              bbox.width, bbox.height)

        x, y = xy_pixel

        ox1, oy1 = x, y

        if self.arrowprops:
            d = self.arrowprops.copy()

            # Use FancyArrowPatch if self.arrowprops has "arrowstyle" key.

            # adjust the starting point of the arrow relative to
            # the textbox.
            # TODO : Rotation needs to be accounted.
            relpos = self._arrow_relpos

            ox0 = bbox.x0 + bbox.width * relpos[0]
            oy0 = bbox.y0 + bbox.height * relpos[1]

            # The arrow will be drawn from (ox0, oy0) to (ox1,
            # oy1). It will be first clipped by patchA and patchB.
            # Then it will be shrunk by shrinkA and shrinkB
            # (in points). If patch A is not set, self.bbox_patch
            # is used.

            self.arrow_patch.set_positions((ox0, oy0), (ox1, oy1))
            fs = self.prop.get_size_in_points()
            mutation_scale = d.pop("mutation_scale", fs)
            mutation_scale = renderer.points_to_pixels(mutation_scale)
            self.arrow_patch.set_mutation_scale(mutation_scale)

            patchA = d.pop("patchA", self.patch)
            self.arrow_patch.set_patchA(patchA)
