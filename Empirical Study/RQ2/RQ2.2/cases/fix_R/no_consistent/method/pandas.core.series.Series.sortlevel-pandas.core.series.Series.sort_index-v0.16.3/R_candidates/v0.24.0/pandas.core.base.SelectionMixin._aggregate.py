    def _aggregate(self, arg, *args, **kwargs):
        """
        provide an implementation for the aggregators

        Parameters
        ----------
        arg : string, dict, function
        *args : args to pass on to the function
        **kwargs : kwargs to pass on to the function

        Returns
        -------
        tuple of result, how

        Notes
        -----
        how can be a string describe the required post-processing, or
        None if not required
        """
        is_aggregator = lambda x: isinstance(x, (list, tuple, dict))
        is_nested_renamer = False

        _axis = kwargs.pop('_axis', None)
        if _axis is None:
            _axis = getattr(self, 'axis', 0)
        _level = kwargs.pop('_level', None)

        if isinstance(arg, compat.string_types):
            return self._try_aggregate_string_function(arg, *args,
                                                       **kwargs), None

        if isinstance(arg, dict):

            # aggregate based on the passed dict
            if _axis != 0:  # pragma: no cover
                raise ValueError('Can only pass dict with axis=0')

            obj = self._selected_obj

            def nested_renaming_depr(level=4):
                # deprecation of nested renaming
                # GH 15931
                warnings.warn(
                    ("using a dict with renaming "
                     "is deprecated and will be removed in a future "
                     "version"),
                    FutureWarning, stacklevel=level)

            # if we have a dict of any non-scalars
            # eg. {'A' : ['mean']}, normalize all to
            # be list-likes
            if any(is_aggregator(x) for x in compat.itervalues(arg)):
                new_arg = compat.OrderedDict()
                for k, v in compat.iteritems(arg):
                    if not isinstance(v, (tuple, list, dict)):
                        new_arg[k] = [v]
                    else:
                        new_arg[k] = v

                    # the keys must be in the columns
                    # for ndim=2, or renamers for ndim=1

                    # ok for now, but deprecated
                    # {'A': { 'ra': 'mean' }}
                    # {'A': { 'ra': ['mean'] }}
                    # {'ra': ['mean']}

                    # not ok
                    # {'ra' : { 'A' : 'mean' }}
                    if isinstance(v, dict):
                        is_nested_renamer = True

                        if k not in obj.columns:
                            msg = ('cannot perform renaming for {key} with a '
                                   'nested dictionary').format(key=k)
                            raise SpecificationError(msg)
                        nested_renaming_depr(4 + (_level or 0))

                    elif isinstance(obj, ABCSeries):
                        nested_renaming_depr()
                    elif (isinstance(obj, ABCDataFrame) and
                          k not in obj.columns):
                        raise KeyError(
                            "Column '{col}' does not exist!".format(col=k))

                arg = new_arg

            else:
                # deprecation of renaming keys
                # GH 15931
                keys = list(compat.iterkeys(arg))
                if (isinstance(obj, ABCDataFrame) and
                        len(obj.columns.intersection(keys)) != len(keys)):
                    nested_renaming_depr()

            from pandas.core.reshape.concat import concat

            def _agg_1dim(name, how, subset=None):
                """
                aggregate a 1-dim with how
                """
                colg = self._gotitem(name, ndim=1, subset=subset)
                if colg.ndim != 1:
                    raise SpecificationError("nested dictionary is ambiguous "
                                             "in aggregation")
                return colg.aggregate(how, _level=(_level or 0) + 1)

            def _agg_2dim(name, how):
                """
                aggregate a 2-dim with how
                """
                colg = self._gotitem(self._selection, ndim=2,
                                     subset=obj)
                return colg.aggregate(how, _level=None)

            def _agg(arg, func):
                """
                run the aggregations over the arg with func
                return an OrderedDict
                """
                result = compat.OrderedDict()
                for fname, agg_how in compat.iteritems(arg):
                    result[fname] = func(fname, agg_how)
                return result

            # set the final keys
            keys = list(compat.iterkeys(arg))
            result = compat.OrderedDict()

            # nested renamer
            if is_nested_renamer:
                result = list(_agg(arg, _agg_1dim).values())

                if all(isinstance(r, dict) for r in result):

                    result, results = compat.OrderedDict(), result
                    for r in results:
                        result.update(r)
                    keys = list(compat.iterkeys(result))

                else:

                    if self._selection is not None:
                        keys = None

            # some selection on the object
            elif self._selection is not None:

                sl = set(self._selection_list)

                # we are a Series like object,
                # but may have multiple aggregations
                if len(sl) == 1:

                    result = _agg(arg, lambda fname,
                                  agg_how: _agg_1dim(self._selection, agg_how))

                # we are selecting the same set as we are aggregating
                elif not len(sl - set(keys)):

                    result = _agg(arg, _agg_1dim)

                # we are a DataFrame, with possibly multiple aggregations
                else:

                    result = _agg(arg, _agg_2dim)

            # no selection
            else:

                try:
                    result = _agg(arg, _agg_1dim)
                except SpecificationError:

                    # we are aggregating expecting all 1d-returns
                    # but we have 2d
                    result = _agg(arg, _agg_2dim)

            # combine results

            def is_any_series():
                # return a boolean if we have *any* nested series
                return any(isinstance(r, ABCSeries)
                           for r in compat.itervalues(result))

            def is_any_frame():
                # return a boolean if we have *any* nested series
                return any(isinstance(r, ABCDataFrame)
                           for r in compat.itervalues(result))

            if isinstance(result, list):
                return concat(result, keys=keys, axis=1, sort=True), True

            elif is_any_frame():
                # we have a dict of DataFrames
                # return a MI DataFrame

                return concat([result[k] for k in keys],
                              keys=keys, axis=1), True

            elif isinstance(self, ABCSeries) and is_any_series():

                # we have a dict of Series
                # return a MI Series
                try:
                    result = concat(result)
                except TypeError:
                    # we want to give a nice error here if
                    # we have non-same sized objects, so
                    # we don't automatically broadcast

                    raise ValueError("cannot perform both aggregation "
                                     "and transformation operations "
                                     "simultaneously")

                return result, True

            # fall thru
            from pandas import DataFrame, Series
            try:
                result = DataFrame(result)
            except ValueError:

                # we have a dict of scalars
                result = Series(result,
                                name=getattr(self, 'name', None))

            return result, True
        elif is_list_like(arg) and arg not in compat.string_types:
            # we require a list, but not an 'str'
            return self._aggregate_multiple_funcs(arg,
                                                  _level=_level,
                                                  _axis=_axis), None
        else:
            result = None

        f = self._is_cython_func(arg)
        if f and not args and not kwargs:
            return getattr(self, f)(), None

        # caller can react
        return result, True
