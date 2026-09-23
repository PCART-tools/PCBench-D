    def _get_data_mask(self, t, f1, f2, where):
        """
        Return a bool array, with True at all points that should eventually be rendered.

        The array is True at a point if none of the data inputs
        *t*, *f1*, *f2* is masked and if the input *where* is true at that point.
        """
        if where is None:
            where = True
        else:
            where = np.asarray(where, dtype=bool)
            if where.size != t.size:
                msg = "where size ({}) does not match {!r} size ({})".format(
                    where.size, self.t_direction, t.size)
                raise ValueError(msg)
        return where & ~functools.reduce(
            np.logical_or, map(np.ma.getmaskarray, [t, f1, f2]))
