    def with_extremes(self, *, bad=None, under=None, over=None):
        """
        Return a copy of the `MultivarColormap` with modified out-of-range attributes.

        The *bad* keyword modifies the copied `MultivarColormap` while *under* and
        *over* modifies the attributes of the copied component colormaps.
        Note that *under* and *over* colors are subject to the mixing rules determined
        by the *combination_mode*.

        Parameters
        ----------
        bad: :mpltype:`color`, default: None
            If Matplotlib color, the bad value is set accordingly in the copy

        under tuple of :mpltype:`color`, default: None
            If tuple, the `under` value of each component is set with the values
            from the tuple.

        over tuple of :mpltype:`color`, default: None
            If tuple, the `over` value of each component is set with the values
            from the tuple.

        Returns
        -------
        MultivarColormap
            copy of self with attributes set

        """
        new_cm = self.copy()
        if bad is not None:
            new_cm._rgba_bad = to_rgba(bad)
        if under is not None:
            if not np.iterable(under) or len(under) != len(new_cm):
                raise ValueError("*under* must contain a color for each scalar colormap"
                                 f" i.e. be of length {len(new_cm)}.")
            else:
                for c, b in zip(new_cm, under):
                    c.set_under(b)
        if over is not None:
            if not np.iterable(over) or len(over) != len(new_cm):
                raise ValueError("*over* must contain a color for each scalar colormap"
                                 f" i.e. be of length {len(new_cm)}.")
            else:
                for c, b in zip(new_cm, over):
                    c.set_over(b)
        return new_cm
