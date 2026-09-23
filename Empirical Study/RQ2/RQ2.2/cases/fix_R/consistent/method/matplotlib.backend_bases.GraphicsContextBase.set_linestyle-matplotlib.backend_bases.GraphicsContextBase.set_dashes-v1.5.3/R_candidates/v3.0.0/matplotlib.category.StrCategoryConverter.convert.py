    @staticmethod
    def convert(value, unit, axis):
        """Converts strings in value to floats using
        mapping information store in the unit object.

        Parameters
        ----------
        value : string or iterable
            value or list of values to be converted
        unit : :class:`.UnitData`
           object string unit information for value
        axis : :class:`~matplotlib.Axis.axis`
            axis on which the converted value is plotted

        Returns
        -------
        mapped_ value : float or ndarray[float]

        .. note:: axis is not used in this function
        """
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
