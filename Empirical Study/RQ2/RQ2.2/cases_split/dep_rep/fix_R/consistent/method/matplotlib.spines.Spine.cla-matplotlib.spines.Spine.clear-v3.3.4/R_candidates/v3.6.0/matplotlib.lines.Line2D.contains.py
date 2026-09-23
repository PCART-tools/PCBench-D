    def contains(self, mouseevent):
        """
        Test whether *mouseevent* occurred on the line.

        An event is deemed to have occurred "on" the line if it is less
        than ``self.pickradius`` (default: 5 points) away from it.  Use
        `~.Line2D.get_pickradius` or `~.Line2D.set_pickradius` to get or set
        the pick radius.

        Parameters
        ----------
        mouseevent : `matplotlib.backend_bases.MouseEvent`

        Returns
        -------
        contains : bool
            Whether any values are within the radius.
        details : dict
            A dictionary ``{'ind': pointlist}``, where *pointlist* is a
            list of points of the line that are within the pickradius around
            the event position.

            TODO: sort returned indices by distance
        """
        inside, info = self._default_contains(mouseevent)
        if inside is not None:
            return inside, info

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
            _log.warning('no figure set when check if mouse is on line')
            pixels = self._pickradius
        else:
            pixels = self.figure.dpi / 72. * self._pickradius

        # The math involved in checking for containment (here and inside of
        # segment_hits) assumes that it is OK to overflow, so temporarily set
        # the error flags accordingly.
        with np.errstate(all='ignore'):
            # Check for collision
            if self._linestyle in ['None', None]:
                # If no line, return the nearby point(s)
                ind, = np.nonzero(
                    (xt - mouseevent.x) ** 2 + (yt - mouseevent.y) ** 2
                    <= pixels ** 2)
            else:
                # If line, return the nearby segment(s)
                ind = segment_hits(mouseevent.x, mouseevent.y, xt, yt, pixels)
                if self._drawstyle.startswith("steps"):
                    ind //= 2

        ind += self.ind_offset

        # Return the point(s) within radius
        return len(ind) > 0, dict(ind=ind)
