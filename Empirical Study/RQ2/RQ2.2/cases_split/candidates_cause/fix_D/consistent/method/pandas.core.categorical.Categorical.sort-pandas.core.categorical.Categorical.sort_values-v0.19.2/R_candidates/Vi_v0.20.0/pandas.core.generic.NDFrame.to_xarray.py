    def to_xarray(self):
        """
        Return an xarray object from the pandas object.

        Returns
        -------
        a DataArray for a Series
        a Dataset for a DataFrame
        a DataArray for higher dims

        Examples
        --------
        >>> df = pd.DataFrame({'A' : [1, 1, 2],
                               'B' : ['foo', 'bar', 'foo'],
                               'C' : np.arange(4.,7)})
        >>> df
           A    B    C
        0  1  foo  4.0
        1  1  bar  5.0
        2  2  foo  6.0

        >>> df.to_xarray()
        <xarray.Dataset>
        Dimensions:  (index: 3)
        Coordinates:
          * index    (index) int64 0 1 2
        Data variables:
            A        (index) int64 1 1 2
            B        (index) object 'foo' 'bar' 'foo'
            C        (index) float64 4.0 5.0 6.0

        >>> df = pd.DataFrame({'A' : [1, 1, 2],
                               'B' : ['foo', 'bar', 'foo'],
                               'C' : np.arange(4.,7)}
                             ).set_index(['B','A'])
        >>> df
                 C
        B   A
        foo 1  4.0
        bar 1  5.0
        foo 2  6.0

        >>> df.to_xarray()
        <xarray.Dataset>
        Dimensions:  (A: 2, B: 2)
        Coordinates:
          * B        (B) object 'bar' 'foo'
          * A        (A) int64 1 2
        Data variables:
            C        (B, A) float64 5.0 nan 4.0 6.0

        >>> p = pd.Panel(np.arange(24).reshape(4,3,2),
                         items=list('ABCD'),
                         major_axis=pd.date_range('20130101', periods=3),
                         minor_axis=['first', 'second'])
        >>> p
        <class 'pandas.core.panel.Panel'>
        Dimensions: 4 (items) x 3 (major_axis) x 2 (minor_axis)
        Items axis: A to D
        Major_axis axis: 2013-01-01 00:00:00 to 2013-01-03 00:00:00
        Minor_axis axis: first to second

        >>> p.to_xarray()
        <xarray.DataArray (items: 4, major_axis: 3, minor_axis: 2)>
        array([[[ 0,  1],
                [ 2,  3],
                [ 4,  5]],
               [[ 6,  7],
                [ 8,  9],
                [10, 11]],
               [[12, 13],
                [14, 15],
                [16, 17]],
               [[18, 19],
                [20, 21],
                [22, 23]]])
        Coordinates:
          * items       (items) object 'A' 'B' 'C' 'D'
          * major_axis  (major_axis) datetime64[ns] 2013-01-01 2013-01-02 2013-01-03  # noqa
          * minor_axis  (minor_axis) object 'first' 'second'

        Notes
        -----
        See the `xarray docs <http://xarray.pydata.org/en/stable/>`__
        """
        import xarray
        if self.ndim == 1:
            return xarray.DataArray.from_series(self)
        elif self.ndim == 2:
            return xarray.Dataset.from_dataframe(self)

        # > 2 dims
        coords = [(a, self._get_axis(a)) for a in self._AXIS_ORDERS]
        return xarray.DataArray(self,
                                coords=coords,
                                )
