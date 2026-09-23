    def contains(self, mouseevent):
        """
        Test whether the mouse event occurred in the collection.

        Returns True | False, ``dict(ind=itemlist)``, where every
        item in itemlist contains the event.
        """
        if callable(self._contains):
            return self._contains(self, mouseevent)

        if not self.get_visible():
            return False, {}

        pickradius = (
            float(self._picker)
            if isinstance(self._picker, Number) and
               self._picker is not True  # the bool, not just nonzero or 1
            else self._pickradius)

        transform, transOffset, offsets, paths = self._prepare_points()

        ind = _path.point_in_path_collection(
            mouseevent.x, mouseevent.y, pickradius,
            transform.frozen(), paths, self.get_transforms(),
            offsets, transOffset, pickradius <= 0,
            self.get_offset_position())

        return len(ind) > 0, dict(ind=ind)
