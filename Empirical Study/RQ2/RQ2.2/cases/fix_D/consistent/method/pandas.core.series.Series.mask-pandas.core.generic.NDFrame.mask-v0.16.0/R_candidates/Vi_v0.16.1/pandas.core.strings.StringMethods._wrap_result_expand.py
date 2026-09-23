    def _wrap_result_expand(self, result, expand=False):
        if not isinstance(expand, bool):
            raise ValueError("expand must be True or False")

        from pandas.core.index import Index, MultiIndex
        if not hasattr(result, 'ndim'):
            return result

        if isinstance(self.series, Index):
            name = getattr(result, 'name', None)
            # if result is a boolean np.array, return the np.array
            # instead of wrapping it into a boolean Index (GH 8875)
            if hasattr(result, 'dtype') and is_bool_dtype(result):
                return result

            if expand:
                result = list(result)
                return MultiIndex.from_tuples(result, names=name)
            else:
                return Index(result, name=name)
        else:
            index = self.series.index
            if expand:
                cons_row = self.series._constructor
                cons = self.series._constructor_expanddim
                data = [cons_row(x) for x in result]
                return cons(data, index=index)
            else:
                name = getattr(result, 'name', None)
                cons = self.series._constructor
                return cons(result, name=name, index=index)
