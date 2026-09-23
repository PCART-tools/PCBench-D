    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred in the collection.

        Returns ``bool, dict(ind=itemlist)``, where every item in itemlist
        contains the event.
        """
        if self._different_canvas(mouseevent) or not self.get_visible():
            return False, {}
        pickradius = (
            float(self._picker)
            if isinstance(self._picker, Number) and
               self._picker is not True  # the bool, not just nonzero or 1
            else self._pickradius)
        if self.axes:
            self.axes._unstale_viewLim()
        transform, offset_trf, offsets, paths = self._prepare_points()
        # Tests if the point is contained on one of the polygons formed
        # by the control points of each of the paths. A point is considered
        # "on" a path if it would lie within a stroke of width 2*pickradius
        # following the path. If pickradius <= 0, then we instead simply check
        # if the point is *inside* of the path instead.
        ind = _path.point_in_path_collection(
            mouseevent.x, mouseevent.y, pickradius,
            transform.frozen(), paths, self.get_transforms(),
            offsets, offset_trf, pickradius <= 0)
        return len(ind) > 0, dict(ind=ind)
