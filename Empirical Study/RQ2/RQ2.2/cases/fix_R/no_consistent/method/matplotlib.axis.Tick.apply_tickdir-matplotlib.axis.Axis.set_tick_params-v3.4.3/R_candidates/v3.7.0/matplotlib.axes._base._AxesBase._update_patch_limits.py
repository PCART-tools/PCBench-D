    def _update_patch_limits(self, patch):
        """Update the data limits for the given patch."""
        # hist can add zero height Rectangles, which is useful to keep
        # the bins, counts and patches lined up, but it throws off log
        # scaling.  We'll ignore rects with zero height or width in
        # the auto-scaling

        # cannot check for '==0' since unitized data may not compare to zero
        # issue #2150 - we update the limits if patch has non zero width
        # or height.
        if (isinstance(patch, mpatches.Rectangle) and
                ((not patch.get_width()) and (not patch.get_height()))):
            return
        p = patch.get_path()
        # Get all vertices on the path
        # Loop through each segment to get extrema for Bezier curve sections
        vertices = []
        for curve, code in p.iter_bezier(simplify=False):
            # Get distance along the curve of any extrema
            _, dzeros = curve.axis_aligned_extrema()
            # Calculate vertices of start, end and any extrema in between
            vertices.append(curve([0, *dzeros, 1]))

        if len(vertices):
            vertices = np.row_stack(vertices)

        patch_trf = patch.get_transform()
        updatex, updatey = patch_trf.contains_branch_seperately(self.transData)
        if not (updatex or updatey):
            return
        if self.name != "rectilinear":
            # As in _update_line_limits, but for axvspan.
            if updatex and patch_trf == self.get_yaxis_transform():
                updatex = False
            if updatey and patch_trf == self.get_xaxis_transform():
                updatey = False
        trf_to_data = patch_trf - self.transData
        xys = trf_to_data.transform(vertices)
        self.update_datalim(xys, updatex=updatex, updatey=updatey)
