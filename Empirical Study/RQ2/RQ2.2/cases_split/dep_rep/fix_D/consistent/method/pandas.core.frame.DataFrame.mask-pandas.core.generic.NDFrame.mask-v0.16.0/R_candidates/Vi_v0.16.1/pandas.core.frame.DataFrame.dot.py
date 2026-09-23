    def dot(self, other):
        """
        Matrix multiplication with DataFrame or Series objects

        Parameters
        ----------
        other : DataFrame or Series

        Returns
        -------
        dot_product : DataFrame or Series
        """
        if isinstance(other, (Series, DataFrame)):
            common = self.columns.union(other.index)
            if (len(common) > len(self.columns) or
                    len(common) > len(other.index)):
                raise ValueError('matrices are not aligned')

            left = self.reindex(columns=common, copy=False)
            right = other.reindex(index=common, copy=False)
            lvals = left.values
            rvals = right.values
        else:
            left = self
            lvals = self.values
            rvals = np.asarray(other)
            if lvals.shape[1] != rvals.shape[0]:
                raise ValueError('Dot product shape mismatch, %s vs %s' %
                                 (lvals.shape, rvals.shape))

        if isinstance(other, DataFrame):
            return self._constructor(np.dot(lvals, rvals),
                                     index=left.index,
                                     columns=other.columns)
        elif isinstance(other, Series):
            return Series(np.dot(lvals, rvals), index=left.index)
        elif isinstance(rvals, (np.ndarray, Index)):
            result = np.dot(lvals, rvals)
            if result.ndim == 2:
                return self._constructor(result, index=left.index)
            else:
                return Series(result, index=left.index)
        else:  # pragma: no cover
            raise TypeError('unsupported type: %s' % type(other))
