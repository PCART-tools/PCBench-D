    def get_values(self):
        """
        Return an ndarray after converting sparse values to dense.

        This is the same as ``.values`` for non-sparse data. For sparse
        data contained in a `pandas.SparseArray`, the data are first
        converted to a dense representation.

        Returns
        -------
        numpy.ndarray
            Numpy representation of DataFrame

        See Also
        --------
        values : Numpy representation of DataFrame.
        pandas.SparseArray : Container for sparse data.

        Examples
        --------
        >>> df = pd.DataFrame({'a': [1, 2], 'b': [True, False],
        ...                    'c': [1.0, 2.0]})
        >>> df
           a      b    c
        0  1   True  1.0
        1  2  False  2.0

        >>> df.get_values()
        array([[1, True, 1.0], [2, False, 2.0]], dtype=object)

        >>> df = pd.DataFrame({"a": pd.SparseArray([1, None, None]),
        ...                    "c": [1.0, 2.0, 3.0]})
        >>> df
             a    c
        0  1.0  1.0
        1  NaN  2.0
        2  NaN  3.0

        >>> df.get_values()
        array([[ 1.,  1.],
               [nan,  2.],
               [nan,  3.]])
        """
        return self.values
