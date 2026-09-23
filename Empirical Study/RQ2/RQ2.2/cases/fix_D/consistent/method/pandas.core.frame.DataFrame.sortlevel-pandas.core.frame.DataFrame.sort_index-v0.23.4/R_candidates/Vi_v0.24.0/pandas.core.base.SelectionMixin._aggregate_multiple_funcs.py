    def _aggregate_multiple_funcs(self, arg, _level, _axis):
        from pandas.core.reshape.concat import concat

        if _axis != 0:
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
                    name = com.get_callable_name(a) or a
                    keys.append(name)
                except (TypeError, DataError):
                    pass
                except SpecificationError:
                    raise

        # multiples
        else:
            for index, col in enumerate(obj):
                try:
                    colg = self._gotitem(col, ndim=1,
                                         subset=obj.iloc[:, index])
                    results.append(colg.aggregate(arg))
                    keys.append(col)
                except (TypeError, DataError):
                    pass
                except ValueError:
                    # cannot aggregate
                    continue
                except SpecificationError:
                    raise

        # if we are empty
        if not len(results):
            raise ValueError("no results")

        try:
            return concat(results, keys=keys, axis=1, sort=False)
        except TypeError:

            # we are concatting non-NDFrame objects,
            # e.g. a list of scalars

            from pandas.core.dtypes.cast import is_nested_object
            from pandas import Series
            result = Series(results, index=keys, name=self.name)
            if is_nested_object(result):
                raise ValueError("cannot combine transform and "
                                 "aggregation operations")
            return result
