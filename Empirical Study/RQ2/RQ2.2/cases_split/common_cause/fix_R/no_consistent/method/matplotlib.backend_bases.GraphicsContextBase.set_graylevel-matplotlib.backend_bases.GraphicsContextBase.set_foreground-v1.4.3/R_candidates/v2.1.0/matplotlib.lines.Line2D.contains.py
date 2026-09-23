    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred on the line.  The pick
        radius determines the precision of the location test (usually
        within five points of the value).  Use
        :meth:`~matplotlib.lines.Line2D.get_pickradius` or
        :meth:`~matplotlib.lines.Line2D.set_pickradius` to view or
        modify it.

        Returns *True* if any values are within the radius along with
        ``{'ind': pointlist}``, where *pointlist* is the set of points
        within the radius.

        TODO: sort returned indices by distance
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)

        if not is_numlike(self.pickradius):
            raise ValueError("pick radius should be a distance")

        # Make sure we have data to plot
        if self._invalidy or self._invalidx:
            self.recache()
        if len(self._xy) == 0:
            return False, {}

        # Convert points to pixels
        transformed_path = self._get_transformed_path()
        path, affine = transformed_path.get_transformed_path_and_affine()
        path = affine.transform_path(path)
        xy = path.vertices
        xt = xy[:, 0]
        yt = xy[:, 1]

        # Convert pick radius from points to pixels
        if self.figure is None:
            warnings.warn('no figure set when check if mouse is on line')
            pixels = self.pickradius
        else:
            pixels = self.figure.dpi / 72. * self.pickradius

        # the math involved in checking for containment (here and inside of
        # segment_hits) assumes that it is OK to overflow.  In case the
        # application has set the error flags such that an exception is raised
        # on overflow, we temporarily set the appropriate error flags here and
        # set them back when we are finished.
        with np.errstate(all='ignore'):
            # Check for collision
            if self._linestyle in ['None', None]:
                # If no line, return the nearby point(s)
                d = (xt - mouseevent.x) ** 2 + (yt - mouseevent.y) ** 2
                ind, = np.nonzero(np.less_equal(d, pixels ** 2))
            else:
                # If line, return the nearby segment(s)
                ind = segment_hits(mouseevent.x, mouseevent.y, xt, yt, pixels)
                if self._drawstyle.startswith("steps"):
                    ind //= 2

        ind += self.ind_offset

        # Return the point(s) within radius
        return len(ind) > 0, dict(ind=ind)
