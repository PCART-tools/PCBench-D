    def calc_label_rot_and_inline(self, slc, ind, lw, lc=None, spacing=5):
        """
        This function calculates the appropriate label rotation given
        the linecontour coordinates in screen units, the index of the
        label location and the label width.

        It will also break contour and calculate inlining if *lc* is
        not empty (lc defaults to the empty list if None).  *spacing*
        is the space around the label in pixels to leave empty.

        Do both of these tasks at once to avoid calling mlab.path_length
        multiple times, which is relatively costly.

        The method used here involves calculating the path length
        along the contour in pixel coordinates and then looking
        approximately label width / 2 away from central point to
        determine rotation and then to break contour if desired.
        """

        if lc is None:
            lc = []
        # Half the label width
        hlw = lw / 2.0

        # Check if closed and, if so, rotate contour so label is at edge
        closed = mlab.is_closed_polygon(slc)
        if closed:
            slc = np.r_[slc[ind:-1], slc[:ind + 1]]

            if len(lc):  # Rotate lc also if not empty
                lc = np.r_[lc[ind:-1], lc[:ind + 1]]

            ind = 0

        # Path length in pixel space
        pl = mlab.path_length(slc)
        pl = pl - pl[ind]

        # Use linear interpolation to get points around label
        xi = np.array([-hlw, hlw])
        if closed:  # Look at end also for closed contours
            dp = np.array([pl[-1], 0])
        else:
            dp = np.zeros_like(xi)

        ll = mlab.less_simple_linear_interpolation(pl, slc, dp + xi,
                                                   extrap=True)

        # get vector in pixel space coordinates from one point to other
        dd = np.diff(ll, axis=0).ravel()

        # Get angle of vector - must be calculated in pixel space for
        # text rotation to work correctly
        if np.all(dd == 0):  # Must deal with case of zero length label
            rotation = 0.0
        else:
            rotation = np.rad2deg(np.arctan2(dd[1], dd[0]))

        if self.rightside_up:
            # Fix angle so text is never upside-down
            if rotation > 90:
                rotation = rotation - 180.0
            if rotation < -90:
                rotation = 180.0 + rotation

        # Break contour if desired
        nlc = []
        if len(lc):
            # Expand range by spacing
            xi = dp + xi + np.array([-spacing, spacing])

            # Get indices near points of interest
            I = mlab.less_simple_linear_interpolation(
                pl, np.arange(len(pl)), xi, extrap=False)

            # If those indices aren't beyond contour edge, find x,y
            if (not np.isnan(I[0])) and int(I[0]) != I[0]:
                xy1 = mlab.less_simple_linear_interpolation(
                    pl, lc, [xi[0]])

            if (not np.isnan(I[1])) and int(I[1]) != I[1]:
                xy2 = mlab.less_simple_linear_interpolation(
                    pl, lc, [xi[1]])

            # Round to integer values but keep as float
            # To allow check against nan below
            # Ignore nans here to avoid throwing an error on Appveyor build
            # (can possibly be removed when build uses numpy 1.13)
            with np.errstate(invalid='ignore'):
                I = [np.floor(I[0]), np.ceil(I[1])]

            # Actually break contours
            if closed:
                # This will remove contour if shorter than label
                if np.all(~np.isnan(I)):
                    nlc.append(np.r_[xy2, lc[int(I[1]):int(I[0]) + 1], xy1])
            else:
                # These will remove pieces of contour if they have length zero
                if not np.isnan(I[0]):
                    nlc.append(np.r_[lc[:int(I[0]) + 1], xy1])
                if not np.isnan(I[1]):
                    nlc.append(np.r_[xy2, lc[int(I[1]):]])

            # The current implementation removes contours completely
            # covered by labels.  Uncomment line below to keep
            # original contour if this is the preferred behavior.
            # if not len(nlc): nlc = [ lc ]

        return rotation, nlc
