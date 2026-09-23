    @staticmethod
    def default_units(data, axis):
        """Sets and updates the :class:`~matplotlib.Axis.axis` units.

        Parameters
        ----------
        data : string or iterable of strings
        axis : :class:`~matplotlib.Axis.axis`
            axis on which the data is plotted

        Returns
        -------
        class:~.UnitData~
            object storing string to integer mapping
        """
        # the conversion call stack is supposed to be
        # default_units->axis_info->convert
        if axis.units is None:
            axis.set_units(UnitData(data))
        else:
            axis.units.update(data)
        return axis.units
