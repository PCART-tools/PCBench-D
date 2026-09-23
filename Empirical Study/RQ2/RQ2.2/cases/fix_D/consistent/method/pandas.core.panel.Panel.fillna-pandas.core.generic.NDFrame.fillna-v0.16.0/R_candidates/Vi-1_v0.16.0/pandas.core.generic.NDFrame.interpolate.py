    def interpolate(self, method='linear', axis=0, limit=None, inplace=False,
                    downcast=None, **kwargs):
        """
        Interpolate values according to different methods.

        Parameters
        ----------
        method : {'linear', 'time', 'index', 'values', 'nearest', 'zero',
                  'slinear', 'quadratic', 'cubic', 'barycentric', 'krogh',
                  'polynomial', 'spline' 'piecewise_polynomial', 'pchip'}

            * 'linear': ignore the index and treat the values as equally
              spaced. default
            * 'time': interpolation works on daily and higher resolution
              data to interpolate given length of interval
            * 'index', 'values': use the actual numerical values of the index
            * 'nearest', 'zero', 'slinear', 'quadratic', 'cubic',
              'barycentric', 'polynomial' is passed to
              `scipy.interpolate.interp1d` with the order given both
              'polynomial' and 'spline' requre that you also specify and order
              (int) e.g. df.interpolate(method='polynomial', order=4)
            * 'krogh', 'piecewise_polynomial', 'spline', and 'pchip' are all
              wrappers around the scipy interpolation methods of similar
              names. See the scipy documentation for more on their behavior:
              http://docs.scipy.org/doc/scipy/reference/interpolate.html#univariate-interpolation
              http://docs.scipy.org/doc/scipy/reference/tutorial/interpolate.html

        axis : {0, 1}, default 0
            * 0: fill column-by-column
            * 1: fill row-by-row
        limit : int, default None.
            Maximum number of consecutive NaNs to fill.
        inplace : bool, default False
            Update the NDFrame in place if possible.
        downcast : optional, 'infer' or None, defaults to None
            Downcast dtypes if possible.

        Returns
        -------
        Series or DataFrame of same shape interpolated at the NaNs

        See Also
        --------
        reindex, replace, fillna

        Examples
        --------

        # Filling in NaNs:
        >>> s = pd.Series([0, 1, np.nan, 3])
        >>> s.interpolate()
        0    0
        1    1
        2    2
        3    3
        dtype: float64

        """
        if self.ndim > 2:
            raise NotImplementedError("Interpolate has not been implemented "
                                      "on Panel and Panel 4D objects.")

        if axis == 0:
            ax = self._info_axis_name
        elif axis == 1:
            self = self.T
            ax = 1
        ax = self._get_axis_number(ax)

        if self.ndim == 2:
            alt_ax = 1 - ax
        else:
            alt_ax = ax

        if isinstance(self.index, MultiIndex) and method != 'linear':
            raise ValueError("Only `method=linear` interpolation is supported "
                             "on MultiIndexes.")

        if self._data.get_dtype_counts().get('object') == len(self.T):
            raise TypeError("Cannot interpolate with all NaNs.")

        # create/use the index
        if method == 'linear':
            index = np.arange(len(self._get_axis(alt_ax)))  # prior default
        else:
            index = self._get_axis(alt_ax)

        if pd.isnull(index).any():
            raise NotImplementedError("Interpolation with NaNs in the index "
                                      "has not been implemented. Try filling "
                                      "those NaNs before interpolating.")
        new_data = self._data.interpolate(method=method,
                                          axis=ax,
                                          index=index,
                                          values=self,
                                          limit=limit,
                                          inplace=inplace,
                                          downcast=downcast,
                                          **kwargs)
        if inplace:
            if axis == 1:
                self._update_inplace(new_data)
                self = self.T
            else:
                self._update_inplace(new_data)
        else:
            res = self._constructor(new_data).__finalize__(self)
            if axis == 1:
                res = res.T
            return res
