    @classmethod
    def _add_series_only_operations(cls):
        """
        Add the series only operations to the cls; evaluate the doc
        strings again.
        """

        axis_descr, name, name2 = _doc_parms(cls)

        def nanptp(values, axis=0, skipna=True):
            nmax = nanops.nanmax(values, axis, skipna)
            nmin = nanops.nanmin(values, axis, skipna)
            warnings.warn(
                "Method .ptp is deprecated and will be removed "
                "in a future version. Use numpy.ptp instead.",
                FutureWarning,
                stacklevel=4,
            )
            return nmax - nmin

        cls.ptp = _make_stat_function(
            cls,
            "ptp",
            name,
            name2,
            axis_descr,
            """Return the difference between the maximum value and the
            minimum value in the object. This is the equivalent of the
            ``numpy.ndarray`` method ``ptp``.\n\n.. deprecated:: 0.24.0
                Use numpy.ptp instead""",
            nanptp,
        )
