    def _reindex_multi(self, axes, copy, fill_value):
        """ we are guaranteed non-Nones in the axes! """

        new_index, row_indexer = self.index.reindex(axes['index'])
        new_columns, col_indexer = self.columns.reindex(axes['columns'])

        if row_indexer is not None and col_indexer is not None:
            indexer = row_indexer, col_indexer
            new_values = algos.take_2d_multi(self.values, indexer,
                                             fill_value=fill_value)
            return self._constructor(new_values, index=new_index,
                                     columns=new_columns)
        else:
            return self._reindex_with_indexers({0: [new_index, row_indexer],
                                                1: [new_columns, col_indexer]},
                                               copy=copy,
                                               fill_value=fill_value)
