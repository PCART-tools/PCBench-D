    def _aggregate_multiple_funcs(self, arg):
        from pandas.tools.merge import concat

        if self.axis != 0:
            raise NotImplementedError

        obj = self._obj_with_exclusions

        results = []
        keys = []
        for col in obj:
            try:
                colg = SeriesGroupBy(obj[col], selection=col,
                                     grouper=self.grouper)
                results.append(colg.aggregate(arg))
                keys.append(col)
            except (TypeError, DataError):
                pass
            except SpecificationError:
                raise
        result = concat(results, keys=keys, axis=1)

        return result
