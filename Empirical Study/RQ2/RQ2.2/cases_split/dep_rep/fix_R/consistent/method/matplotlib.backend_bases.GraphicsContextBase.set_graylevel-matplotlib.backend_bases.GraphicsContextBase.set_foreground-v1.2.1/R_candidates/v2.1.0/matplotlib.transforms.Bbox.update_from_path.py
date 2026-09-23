    def update_from_path(self, path, ignore=None, updatex=True, updatey=True):
        """
        Update the bounds of the :class:`Bbox` based on the passed in
        data.  After updating, the bounds will have positive *width*
        and *height*; *x0* and *y0* will be the minimal values.

        *path*: a :class:`~matplotlib.path.Path` instance

        *ignore*:
           - when True, ignore the existing bounds of the :class:`Bbox`.
           - when False, include the existing bounds of the :class:`Bbox`.
           - when None, use the last value passed to :meth:`ignore`.

        *updatex*: when True, update the x values

        *updatey*: when True, update the y values

        """
        if ignore is None:
            ignore = self._ignore

        if path.vertices.size == 0:
            return

        points, minpos, changed = update_path_extents(
            path, None, self._points, self._minpos, ignore)

        if changed:
            self.invalidate()
            if updatex:
                self._points[:, 0] = points[:, 0]
                self._minpos[0] = minpos[0]
            if updatey:
                self._points[:, 1] = points[:, 1]
                self._minpos[1] = minpos[1]
