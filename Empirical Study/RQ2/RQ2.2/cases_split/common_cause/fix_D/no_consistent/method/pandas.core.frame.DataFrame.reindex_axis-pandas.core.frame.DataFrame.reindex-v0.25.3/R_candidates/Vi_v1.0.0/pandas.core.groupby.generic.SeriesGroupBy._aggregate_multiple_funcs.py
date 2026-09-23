    def _aggregate_multiple_funcs(self, arg):
        if isinstance(arg, dict):

            # show the deprecation, but only if we
            # have not shown a higher level one
            # GH 15931
            if isinstance(self._selected_obj, Series):
                raise SpecificationError("nested renamer is not supported")

            columns = list(arg.keys())
            arg = arg.items()
        elif any(isinstance(x, (tuple, list)) for x in arg):
            arg = [(x, x) if not isinstance(x, (tuple, list)) else x for x in arg]

            # indicated column order
            columns = next(zip(*arg))
        else:
            # list of functions / function names
            columns = []
            for f in arg:
                columns.append(com.get_callable_name(f) or f)

            arg = zip(columns, arg)

        results = {}
        for name, func in arg:
            obj = self

            # reset the cache so that we
            # only include the named selection
            if name in self._selected_obj:
                obj = copy.copy(obj)
                obj._reset_cache()
                obj._selection = name
            results[name] = obj.aggregate(func)

        if any(isinstance(x, DataFrame) for x in results.values()):
            # let higher level handle
            return results

        return DataFrame(results, columns=columns)
