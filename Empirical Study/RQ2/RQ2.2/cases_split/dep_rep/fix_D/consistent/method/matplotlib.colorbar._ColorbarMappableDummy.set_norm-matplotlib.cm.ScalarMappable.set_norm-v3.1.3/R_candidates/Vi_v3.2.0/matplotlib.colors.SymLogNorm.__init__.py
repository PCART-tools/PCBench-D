    def __init__(self, linthresh, linscale=1.0, vmin=None, vmax=None,
                 clip=False, *, base=None):
        """
        Parameters
        ----------
        linthresh : float
            The range within which the plot is linear (to avoid having the plot
            go to infinity around zero).
        linscale : float, default: 1
            This allows the linear range (-*linthresh* to *linthresh*)
            to be stretched relative to the logarithmic range. Its
            value is the number of powers of *base* to use for each
            half of the linear range.

            For example, when *linscale* == 1.0 (the default) and
            ``base=10``, then space used for the positive and negative
            halves of the linear range will be equal to a decade in
            the logarithmic.

        base : float, default: None
            If not given, defaults to ``np.e`` (consistent with prior
            behavior) and warns.

            In v3.3 the default value will change to 10 to be consistent with
            `.SymLogNorm`.

            To suppress the warning pass *base* as a keyword argument.

        """
        Normalize.__init__(self, vmin, vmax, clip)
        if base is None:
            self._base = np.e
            cbook.warn_deprecated("3.3", message="default base may change "
                "from np.e to 10.  To suppress this warning specify the base "
                "keyword argument.")
        else:
            self._base = base
        self._log_base = np.log(self._base)

        self.linthresh = float(linthresh)
        self._linscale_adj = (linscale / (1.0 - self._base ** -1))
        if vmin is not None and vmax is not None:
            self._transform_vmin_vmax()
