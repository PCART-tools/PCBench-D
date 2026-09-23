    def add_label_near(self, x, y, inline=True, inline_spacing=5,
                       transform=None):
        """
        Add a label near the point ``(x, y)``.

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
        transform : `.Transform` or `False`, default: ``self.axes.transData``
            A transform applied to ``(x, y)`` before labeling.  The default
            causes ``(x, y)`` to be interpreted as data coordinates.  `False`
            is a synonym for `.IdentityTransform`; i.e. ``(x, y)`` should be
            interpreted as display coordinates.
        """

        if transform is None:
            transform = self.axes.transData
        if transform:
            x, y = transform.transform((x, y))

        # find the nearest contour _in screen units_
        conmin, segmin, imin, xmin, ymin = self.find_nearest_contour(
            x, y, self.labelIndiceList)[:5]

        # calc_label_rot_and_inline() requires that (xmin, ymin)
        # be a vertex in the path. So, if it isn't, add a vertex here
        paths = self.collections[conmin].get_paths()  # paths of correct coll.
        lc = paths[segmin].vertices  # vertices of correct segment
        # Where should the new vertex be added in data-units?
        xcmin = self.axes.transData.inverted().transform([xmin, ymin])
        if not np.allclose(xcmin, lc[imin]):
            # No vertex is close enough, so add a new point in the vertices and
            # replace the path by the new one.
            lc = np.insert(lc, imin, xcmin, axis=0)
            paths[segmin] = mpath.Path(lc)

        # Get index of nearest level in subset of levels used for labeling
        lmin = self.labelIndiceList.index(conmin)

        # Get label width for rotating labels and breaking contours
        lw = self._get_nth_label_width(lmin)

        # Figure out label rotation.
        rotation, nlc = self.calc_label_rot_and_inline(
            self.axes.transData.transform(lc),  # to pixel space.
            imin, lw, lc if inline else None, inline_spacing)

        self.add_label(xmin, ymin, rotation, self.labelLevelList[lmin],
                       self.labelCValueList[lmin])

        if inline:
            # Remove old, not looping over paths so we can do this up front
            paths.pop(segmin)

            # Add paths if not empty or single point
            paths.extend([mpath.Path(n) for n in nlc if len(n) > 1])
