    @property
    def components(self):
        """
        Return a Dataframe of the components of the Timedeltas.

        Returns
        -------
        DataFrame

        Examples
        --------
        >>> s = pd.Series(pd.to_timedelta(np.arange(5), unit='s'))
        >>> s
        0   00:00:00
        1   00:00:01
        2   00:00:02
        3   00:00:03
        4   00:00:04
        dtype: timedelta64[ns]
        >>> s.dt.components
           days  hours  minutes  seconds  milliseconds  microseconds  nanoseconds
        0     0      0        0        0             0             0            0
        1     0      0        0        1             0             0            0
        2     0      0        0        2             0             0            0
        3     0      0        0        3             0             0            0
        4     0      0        0        4             0             0            0
        """  # noqa: E501
        return self._get_values().components.set_index(self._parent.index)
