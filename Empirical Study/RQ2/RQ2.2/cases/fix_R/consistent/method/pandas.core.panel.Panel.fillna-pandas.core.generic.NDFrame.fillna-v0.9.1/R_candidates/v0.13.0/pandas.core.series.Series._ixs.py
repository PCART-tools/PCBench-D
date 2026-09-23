    def _ixs(self, i, axis=0):
        """
        Return the i-th value or values in the Series by location

        Parameters
        ----------
        i : int, slice, or sequence of integers

        Returns
        -------
        value : scalar (int) or Series (slice, sequence)
        """
        try:
            return _index.get_value_at(self.values, i)
        except IndexError:
            raise
        except:
            if isinstance(i, slice):
                indexer = self.index._convert_slice_indexer(i, typ='iloc')
                return self._get_values(indexer)
            else:
                label = self.index[i]
                if isinstance(label, Index):
                    i = _maybe_convert_indices(i, len(self))
                    return self.reindex(i, takeable=True)
                else:
                    return _index.get_value_at(self, i)
