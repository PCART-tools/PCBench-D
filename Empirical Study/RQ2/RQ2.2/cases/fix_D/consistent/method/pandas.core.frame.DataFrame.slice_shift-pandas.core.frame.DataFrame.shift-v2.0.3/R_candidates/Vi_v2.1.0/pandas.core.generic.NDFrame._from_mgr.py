    @classmethod
    def _from_mgr(cls, mgr: Manager, axes: list[Index]) -> Self:
        """
        Construct a new object of this type from a Manager object and axes.

        Parameters
        ----------
        mgr : Manager
            Must have the same ndim as cls.
        axes : list[Index]

        Notes
        -----
        The axes must match mgr.axes, but are required for future-proofing
        in the event that axes are refactored out of the Manager objects.
        """
        obj = cls.__new__(cls)
        NDFrame.__init__(obj, mgr)
        return obj
