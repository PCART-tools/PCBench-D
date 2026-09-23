    def to_tuples(self, na_tuple=True):
        """
        Return an Index of tuples of the form (left, right)

        Parameters
        ----------
        na_tuple : boolean, default True
            Returns NA as a tuple if True, ``(nan, nan)``, or just as the NA
            value itself if False, ``nan``.

            .. versionadded:: 0.23.0

        Examples
        --------
        >>>  idx = pd.IntervalIndex.from_arrays([0, np.nan, 2], [1, np.nan, 3])
        >>>  idx.to_tuples()
        Index([(0.0, 1.0), (nan, nan), (2.0, 3.0)], dtype='object')
        >>>  idx.to_tuples(na_tuple=False)
        Index([(0.0, 1.0), nan, (2.0, 3.0)], dtype='object')
        """
        tuples = com._asarray_tuplesafe(zip(self.left, self.right))
        if not na_tuple:
            # GH 18756
            tuples = np.where(~self._isnan, tuples, np.nan)
        return Index(tuples)
