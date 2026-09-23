    def compute(self, method):

        from pandas import Int64Index
        n = self.n
        frame = self.obj
        columns = self.columns

        for column in columns:
            dtype = frame[column].dtype
            if not self.is_valid_dtype_n_method(dtype):
                raise TypeError((
                    "Column {column!r} has dtype {dtype}, cannot use method "
                    "{method!r} with this dtype"
                ).format(column=column, dtype=dtype, method=method))

        def get_indexer(current_indexer, other_indexer):
            """Helper function to concat `current_indexer` and `other_indexer`
            depending on `method`
            """
            if method == 'nsmallest':
                return current_indexer.append(other_indexer)
            else:
                return other_indexer.append(current_indexer)

        # Below we save and reset the index in case index contains duplicates
        original_index = frame.index
        cur_frame = frame = frame.reset_index(drop=True)
        cur_n = n
        indexer = Int64Index([])

        for i, column in enumerate(columns):

            # For each column we apply method to cur_frame[column].
            # If it is the last column in columns, or if the values
            # returned are unique in frame[column] we save this index
            # and break
            # Otherwise we must save the index of the non duplicated values
            # and set the next cur_frame to cur_frame filtered on all
            # duplcicated values (#GH15297)
            series = cur_frame[column]
            values = getattr(series, method)(cur_n, keep=self.keep)
            is_last_column = len(columns) - 1 == i
            if is_last_column or values.nunique() == series.isin(values).sum():

                # Last column in columns or values are unique in
                # series => values
                # is all that matters
                indexer = get_indexer(indexer, values.index)
                break

            duplicated_filter = series.duplicated(keep=False)
            duplicated = values[duplicated_filter]
            non_duplicated = values[~duplicated_filter]
            indexer = get_indexer(indexer, non_duplicated.index)

            # Must set cur frame to include all duplicated values
            # to consider for the next column, we also can reduce
            # cur_n by the current length of the indexer
            cur_frame = cur_frame[series.isin(duplicated)]
            cur_n = n - len(indexer)

        frame = frame.take(indexer)

        # Restore the index on frame
        frame.index = original_index.take(indexer)
        return frame
