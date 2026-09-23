    @staticmethod
    def axisinfo(unit, axis):
        """Sets the default axis ticks and labels

        Parameters
        ---------
        unit : :class:`.UnitData`
            object string unit information for value
        axis : :class:`~matplotlib.Axis.axis`
            axis for which information is being set

        Returns
        -------
        :class:~matplotlib.units.AxisInfo~
            Information to support default tick labeling

        .. note: axis is not used
        """
        # locator and formatter take mapping dict because
        # args need to be pass by reference for updates
        majloc = StrCategoryLocator(unit._mapping)
        majfmt = StrCategoryFormatter(unit._mapping)
        return units.AxisInfo(majloc=majloc, majfmt=majfmt)
