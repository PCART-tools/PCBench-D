    def _aggregate_multiple_funcs(self, arg, _level):
        from pandas.tools.merge import concat

        if self.axis != 0:
            raise NotImplementedError("axis other than 0 is not supported")

        if self._selected_obj.ndim == 1:
            obj = self._selected_obj
        else:
            obj = self._obj_with_exclusions

        results = []
        keys = []

        # degenerate case
        if obj.ndim == 1:
            for a in arg:
                try:
                    colg = self._gotitem(obj.name, ndim=1, subset=obj)
                    results.append(colg.aggregate(a))

                    # make sure we find a good name
                    name = com._get_callable_name(a) or a
                    keys.append(name)
                except (TypeError, DataError):
                    pass
                except SpecificationError:
                    raise

        # multiples
        else:
            for col in obj:
                try:
                    colg = self._gotitem(col, ndim=1, subset=obj[col])
                    results.append(colg.aggregate(arg))
                    keys.append(col)
                except (TypeError, DataError):
                    pass
                except SpecificationError:
                    raise

        return concat(results, keys=keys, axis=1)
