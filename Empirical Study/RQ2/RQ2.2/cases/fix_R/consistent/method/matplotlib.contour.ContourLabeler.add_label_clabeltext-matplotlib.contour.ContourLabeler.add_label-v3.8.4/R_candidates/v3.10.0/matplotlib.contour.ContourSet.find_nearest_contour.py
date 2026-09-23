    def find_nearest_contour(self, x, y, indices=None, pixel=True):
        """
        Find the point in the contour plot that is closest to ``(x, y)``.

        This method does not support filled contours.

        Parameters
        ----------
        x, y : float
            The reference point.
        indices : list of int or None, default: None
            Indices of contour levels to consider.  If None (the default), all
            levels are considered.
        pixel : bool, default: True
            If *True*, measure distance in pixel (screen) space, which is
            useful for manual contour labeling; else, measure distance in axes
            space.

        Returns
        -------
        path : int
            The index of the path that is closest to ``(x, y)``.  Each path corresponds
            to one contour level.
        subpath : int
            The index within that closest path of the subpath that is closest to
            ``(x, y)``.  Each subpath corresponds to one unbroken contour line.
        index : int
            The index of the vertices within that subpath that are closest to
            ``(x, y)``.
        xmin, ymin : float
            The point in the contour plot that is closest to ``(x, y)``.
        d2 : float
            The squared distance from ``(xmin, ymin)`` to ``(x, y)``.
        """
        segment = index = d2 = None

        with ExitStack() as stack:
            if not pixel:
                # _find_nearest_contour works in pixel space. We want axes space, so
                # effectively disable the transformation here by setting to identity.
                stack.enter_context(self._cm_set(
                    transform=mtransforms.IdentityTransform()))

            i_level, i_vtx, (xmin, ymin) = self._find_nearest_contour((x, y), indices)

        if i_level is not None:
            cc_cumlens = np.cumsum(
                [*map(len, self._paths[i_level]._iter_connected_components())])
            segment = cc_cumlens.searchsorted(i_vtx, "right")
            index = i_vtx if segment == 0 else i_vtx - cc_cumlens[segment - 1]
            d2 = (xmin-x)**2 + (ymin-y)**2

        return (i_level, segment, index, xmin, ymin, d2)
