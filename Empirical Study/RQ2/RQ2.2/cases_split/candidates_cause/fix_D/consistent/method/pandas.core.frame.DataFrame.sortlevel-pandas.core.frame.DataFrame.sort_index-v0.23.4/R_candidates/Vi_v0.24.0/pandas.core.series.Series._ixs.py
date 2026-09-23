    def _ixs(self, i, axis=0):
        """
        Return the i-th value or values in the Series by location.

        Parameters
        ----------
        i : int, slice, or sequence of integers

        Returns
        -------
        value : scalar (int) or Series (slice, sequence)
        """
        try:

            # dispatch to the values if we need
            values = self._values
            if isinstance(values, np.ndarray):
                return libindex.get_value_at(values, i)
            else:
                return values[i]
        except IndexError:
            raise
        except Exception:
            if isinstance(i, slice):
                indexer = self.index._convert_slice_indexer(i, kind='iloc')
                return self._get_values(indexer)
            else:
                label = self.index[i]
                if isinstance(label, Index):
                    return self.take(i, axis=axis, convert=True)
                else:
                    return libindex.get_value_at(self, i)
