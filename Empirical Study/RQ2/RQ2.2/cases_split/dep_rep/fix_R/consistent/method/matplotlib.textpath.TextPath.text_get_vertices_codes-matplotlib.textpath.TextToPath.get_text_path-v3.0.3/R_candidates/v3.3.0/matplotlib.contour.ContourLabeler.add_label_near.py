    def add_label_near(self, x, y, inline=True, inline_spacing=5,
                       transform=None):
        """
        Add a label near the point (x, y). If transform is None
        (default), (x, y) is in data coordinates; if transform is
        False, (x, y) is in display coordinates; otherwise, the
        specified transform will be used to translate (x, y) into
        display coordinates.

        Parameters
        ----------
        x, y : float
            The approximate location of the label.

        inline : bool, default: True
            If *True* remove the segment of the contour beneath the label.

        inline_spacing : int, default: 5
            Space in pixels to leave on each side of label when placing
            inline. This spacing will be exact for labels at locations where
            the contour is straight, less so for labels on curved contours.
        """

        if transform is None:
            transform = self.axes.transData

        if transform:
            x, y = transform.transform((x, y))

        # find the nearest contour _in screen units_
        conmin, segmin, imin, xmin, ymin = self.find_nearest_contour(
            x, y, self.labelIndiceList)[:5]

        # The calc_label_rot_and_inline routine requires that (xmin, ymin)
        # be a vertex in the path. So, if it isn't, add a vertex here

        # grab the paths from the collections
        paths = self.collections[conmin].get_paths()
        # grab the correct segment
        active_path = paths[segmin]
        # grab its vertices
        lc = active_path.vertices
        # sort out where the new vertex should be added data-units
        xcmin = self.axes.transData.inverted().transform([xmin, ymin])
        # if there isn't a vertex close enough
        if not np.allclose(xcmin, lc[imin]):
            # insert new data into the vertex list
            lc = np.row_stack([lc[:imin], xcmin, lc[imin:]])
            # replace the path with the new one
            paths[segmin] = mpath.Path(lc)

        # Get index of nearest level in subset of levels used for labeling
        lmin = self.labelIndiceList.index(conmin)

        # Coordinates of contour
        paths = self.collections[conmin].get_paths()
        lc = paths[segmin].vertices

        # In pixel/screen space
        slc = self.axes.transData.transform(lc)

        # Get label width for rotating labels and breaking contours
        lw = self.get_label_width(self.labelLevelList[lmin],
                                  self.labelFmt, self.labelFontSizeList[lmin])
        # lw is in points.
        lw *= self.axes.figure.dpi / 72  # scale to screen coordinates
        # now lw in pixels

        # Figure out label rotation.
        rotation, nlc = self.calc_label_rot_and_inline(
            slc, imin, lw, lc if inline else None, inline_spacing)

        self.add_label(xmin, ymin, rotation, self.labelLevelList[lmin],
                       self.labelCValueList[lmin])

        if inline:
            # Remove old, not looping over paths so we can do this up front
            paths.pop(segmin)

            # Add paths if not empty or single point
            for n in nlc:
                if len(n) > 1:
                    paths.append(mpath.Path(n))
