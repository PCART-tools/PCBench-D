    def _init_spmatrix(self, data, index, columns, dtype=None,
                       fill_value=None):
        """ Init self from scipy.sparse matrix """
        index, columns = self._prep_index(data, index, columns)
        data = data.tocoo()
        N = len(index)

        # Construct a dict of SparseSeries
        sdict = {}
        values = Series(data.data, index=data.row, copy=False)
        for col, rowvals in values.groupby(data.col):
            # get_blocks expects int32 row indices in sorted order
            rows = rowvals.index.values.astype(np.int32)
            rows.sort()
            blocs, blens = get_blocks(rows)

            sdict[columns[col]] = SparseSeries(
                rowvals.values, index=index,
                fill_value=fill_value,
                sparse_index=BlockIndex(N, blocs, blens))

        # Add any columns that were empty and thus not grouped on above
        sdict.update({column: SparseSeries(index=index,
                                           fill_value=fill_value,
                                           sparse_index=BlockIndex(N, [], []))
                      for column in columns
                      if column not in sdict})

        return self._init_dict(sdict, index, columns, dtype)
