    @staticmethod
    def convert(value, unit, axis):
        """Convert strings in value to floats using
        mapping information store in the unit object.

        Parameters
        ----------
        value : string or iterable
            Value or list of values to be converted.
        unit : `.UnitData`
            An object mapping strings to integers.
        axis : `~matplotlib.axis.Axis`
            axis on which the converted value is plotted.

            .. note:: *axis* is unused.

        Returns
        -------
        mapped_value : float or ndarray[float]
        """
        if unit is None:
            raise ValueError(
                'Missing category information for StrCategoryConverter; '
                'this might be caused by unintendedly mixing categorical and '
                'numeric data')

        # dtype = object preserves numerical pass throughs
        values = np.atleast_1d(np.array(value, dtype=object))

        # pass through sequence of non binary numbers
        if all((units.ConversionInterface.is_numlike(v) and
                not isinstance(v, (str, bytes))) for v in values):
            return np.asarray(values, dtype=float)

        # force an update so it also does type checking
        unit.update(values)

        str2idx = np.vectorize(unit._mapping.__getitem__,
                               otypes=[float])

        mapped_value = str2idx(values)
        return mapped_value
