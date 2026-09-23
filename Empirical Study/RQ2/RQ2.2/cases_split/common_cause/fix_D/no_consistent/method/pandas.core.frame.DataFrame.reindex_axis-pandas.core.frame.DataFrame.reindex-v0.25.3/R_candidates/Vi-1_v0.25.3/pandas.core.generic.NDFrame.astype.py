    def astype(self, dtype, copy=True, errors="raise", **kwargs):
        """
        Cast a pandas object to a specified dtype ``dtype``.

        Parameters
        ----------
        dtype : data type, or dict of column name -> data type
            Use a numpy.dtype or Python type to cast entire pandas object to
            the same type. Alternatively, use {col: dtype, ...}, where col is a
            column label and dtype is a numpy.dtype or Python type to cast one
            or more of the DataFrame's columns to column-specific types.
        copy : bool, default True
            Return a copy when ``copy=True`` (be very careful setting
            ``copy=False`` as changes to values then may propagate to other
            pandas objects).
        errors : {'raise', 'ignore'}, default 'raise'
            Control raising of exceptions on invalid data for provided dtype.

            - ``raise`` : allow exceptions to be raised
            - ``ignore`` : suppress exceptions. On error return original object

            .. versionadded:: 0.20.0

        kwargs : keyword arguments to pass on to the constructor

        Returns
        -------
        casted : same type as caller

        See Also
        --------
        to_datetime : Convert argument to datetime.
        to_timedelta : Convert argument to timedelta.
        to_numeric : Convert argument to a numeric type.
        numpy.ndarray.astype : Cast a numpy array to a specified type.

        Examples
        --------
        Create a DataFrame:

        >>> d = {'col1': [1, 2], 'col2': [3, 4]}
        >>> df = pd.DataFrame(data=d)
        >>> df.dtypes
        col1    int64
        col2    int64
        dtype: object

        Cast all columns to int32:

        >>> df.astype('int32').dtypes
        col1    int32
        col2    int32
        dtype: object

        Cast col1 to int32 using a dictionary:

        >>> df.astype({'col1': 'int32'}).dtypes
        col1    int32
        col2    int64
        dtype: object

        Create a series:

        >>> ser = pd.Series([1, 2], dtype='int32')
        >>> ser
        0    1
        1    2
        dtype: int32
        >>> ser.astype('int64')
        0    1
        1    2
        dtype: int64

        Convert to categorical type:

        >>> ser.astype('category')
        0    1
        1    2
        dtype: category
        Categories (2, int64): [1, 2]

        Convert to ordered categorical type with custom ordering:

        >>> cat_dtype = pd.api.types.CategoricalDtype(
        ...                     categories=[2, 1], ordered=True)
        >>> ser.astype(cat_dtype)
        0    1
        1    2
        dtype: category
        Categories (2, int64): [2 < 1]

        Note that using ``copy=False`` and changing data on a new
        pandas object may propagate changes:

        >>> s1 = pd.Series([1,2])
        >>> s2 = s1.astype('int64', copy=False)
        >>> s2[0] = 10
        >>> s1  # note that s1[0] has changed too
        0    10
        1     2
        dtype: int64
        """
        if is_dict_like(dtype):
            if self.ndim == 1:  # i.e. Series
                if len(dtype) > 1 or self.name not in dtype:
                    raise KeyError(
                        "Only the Series name can be used for "
                        "the key in Series dtype mappings."
                    )
                new_type = dtype[self.name]
                return self.astype(new_type, copy, errors, **kwargs)

            for col_name in dtype.keys():
                if col_name not in self:
                    raise KeyError(
                        "Only a column name can be used for the "
                        "key in a dtype mappings argument."
                    )
            results = []
            for col_name, col in self.items():
                if col_name in dtype:
                    results.append(
                        col.astype(
                            dtype=dtype[col_name], copy=copy, errors=errors, **kwargs
                        )
                    )
                else:
                    results.append(results.append(col.copy() if copy else col))

        elif is_extension_array_dtype(dtype) and self.ndim > 1:
            # GH 18099/22869: columnwise conversion to extension dtype
            # GH 24704: use iloc to handle duplicate column names
            results = (
                self.iloc[:, i].astype(dtype, copy=copy)
                for i in range(len(self.columns))
            )

        else:
            # else, only a single dtype is given
            new_data = self._data.astype(
                dtype=dtype, copy=copy, errors=errors, **kwargs
            )
            return self._constructor(new_data).__finalize__(self)

        # GH 19920: retain column metadata after concat
        result = pd.concat(results, axis=1, copy=False)
        result.columns = self.columns
        return result
