    def _compare_frame(self, other, func, str_rep):
        # compare_frame assumes self._indexed_same(other)

        import pandas.core.computation.expressions as expressions
        # unique
        if self.columns.is_unique:

            def _compare(a, b):
                return {col: func(a[col], b[col]) for col in a.columns}

            new_data = expressions.evaluate(_compare, str_rep, self, other)
            return self._constructor(data=new_data, index=self.index,
                                     columns=self.columns, copy=False)
        # non-unique
        else:

            def _compare(a, b):
                return {i: func(a.iloc[:, i], b.iloc[:, i])
                        for i, col in enumerate(a.columns)}

            new_data = expressions.evaluate(_compare, str_rep, self, other)
            result = self._constructor(data=new_data, index=self.index,
                                       copy=False)
            result.columns = self.columns
            return result
