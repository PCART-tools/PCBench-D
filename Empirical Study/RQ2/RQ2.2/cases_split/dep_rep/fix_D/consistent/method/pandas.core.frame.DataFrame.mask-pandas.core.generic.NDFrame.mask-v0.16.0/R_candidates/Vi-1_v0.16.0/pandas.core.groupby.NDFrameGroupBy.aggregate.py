    @Appender(_agg_doc)
    def aggregate(self, arg, *args, **kwargs):
        if isinstance(arg, compat.string_types):
            return getattr(self, arg)(*args, **kwargs)

        result = OrderedDict()
        if isinstance(arg, dict):
            if self.axis != 0:  # pragma: no cover
                raise ValueError('Can only pass dict with axis=0')

            obj = self._selected_obj

            if any(isinstance(x, (list, tuple, dict)) for x in arg.values()):
                new_arg = OrderedDict()
                for k, v in compat.iteritems(arg):
                    if not isinstance(v, (tuple, list, dict)):
                        new_arg[k] = [v]
                    else:
                        new_arg[k] = v
                arg = new_arg

            keys = []
            if self._selection is not None:
                subset = obj
                if isinstance(subset, DataFrame):
                    raise NotImplementedError

                for fname, agg_how in compat.iteritems(arg):
                    colg = SeriesGroupBy(subset, selection=self._selection,
                                         grouper=self.grouper)
                    result[fname] = colg.aggregate(agg_how)
                    keys.append(fname)
            else:
                for col, agg_how in compat.iteritems(arg):
                    colg = SeriesGroupBy(obj[col], selection=col,
                                         grouper=self.grouper)
                    result[col] = colg.aggregate(agg_how)
                    keys.append(col)

            if isinstance(list(result.values())[0], DataFrame):
                from pandas.tools.merge import concat
                result = concat([result[k] for k in keys], keys=keys, axis=1)
            else:
                result = DataFrame(result)
        elif isinstance(arg, list):
            return self._aggregate_multiple_funcs(arg)
        else:
            cyfunc = _intercept_cython(arg)
            if cyfunc and not args and not kwargs:
                return getattr(self, cyfunc)()

            if self.grouper.nkeys > 1:
                return self._python_agg_general(arg, *args, **kwargs)
            else:

                # try to treat as if we are passing a list
                try:
                    assert not args and not kwargs
                    result = self._aggregate_multiple_funcs([arg])
                    result.columns = Index(result.columns.levels[0],
                                           name=self._selected_obj.columns.name)
                except:
                    result = self._aggregate_generic(arg, *args, **kwargs)

        if not self.as_index:
            self._insert_inaxis_grouper_inplace(result)
            result.index = np.arange(len(result))

        return result.convert_objects()
