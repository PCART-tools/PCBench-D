    def argsort(self, axis=0, kind='quicksort', order=None):
        """
        Overrides ndarray.argsort. Argsorts the value, omitting NA/null values,
        and places the result in the same locations as the non-NA values

        Parameters
        ----------
        axis : int (can only be zero)
        kind : {'mergesort', 'quicksort', 'heapsort'}, default 'quicksort'
            Choice of sorting algorithm. See np.sort for more
            information. 'mergesort' is the only stable algorithm
        order : ignored

        Returns
        -------
        argsorted : Series, with -1 indicated where nan values are present

        """
        values = self.values
        mask = isnull(values)

        if mask.any():
            result = Series(
                -1, index=self.index, name=self.name, dtype='int64')
            notmask = ~mask
            result[notmask] = np.argsort(values[notmask], kind=kind)
            return self._constructor(result,
                                     index=self.index).__finalize__(self)
        else:
            return self._constructor(
                np.argsort(values, kind=kind), index=self.index,
                dtype='int64').__finalize__(self)
