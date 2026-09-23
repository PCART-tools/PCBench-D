    def _convert_to_indexer(self, obj, axis=0, is_setter=False):
        """
        Convert indexing key into something we can use to do actual fancy
        indexing on an ndarray

        Examples
        ix[:5] -> slice(0, 5)
        ix[[1,2,3]] -> [1,2,3]
        ix[['foo', 'bar', 'baz']] -> [i, j, k] (indices of foo, bar, baz)

        Going by Zen of Python?
        "In the face of ambiguity, refuse the temptation to guess."
        raise AmbiguousIndexError with integer labels?
        - No, prefer label-based indexing
        """
        labels = self.obj._get_axis(axis)

        # if we are a scalar indexer and not type correct raise
        obj = self._convert_scalar_indexer(obj, axis)

        # see if we are positional in nature
        is_int_index = labels.is_integer()
        is_int_positional = com.is_integer(obj) and not is_int_index

        # if we are a label return me
        try:
            return labels.get_loc(obj)
        except (KeyError, TypeError):
            pass
        except (ValueError):
            if not is_int_positional:
                raise

        # a positional
        if is_int_positional:

            # if we are setting and its not a valid location
            # its an insert which fails by definition
            if is_setter:

                # always valid
                if self.name == 'loc':
                    return {'key': obj}

                # a positional
                if obj >= len(self.obj) and not isinstance(labels, MultiIndex):
                    raise ValueError("cannot set by positional indexing with "
                                     "enlargement")

            return obj

        if isinstance(obj, slice):
            return self._convert_slice_indexer(obj, axis)

        elif _is_list_like(obj):
            if com._is_bool_indexer(obj):
                obj = _check_bool_indexer(labels, obj)
                inds, = obj.nonzero()
                return inds
            else:
                if isinstance(obj, Index):
                    objarr = obj.values
                else:
                    objarr = _asarray_tuplesafe(obj)

                # If have integer labels, defer to label-based indexing
                if is_integer_dtype(objarr) and not is_int_index:
                    if labels.inferred_type != 'integer':
                        objarr = np.where(objarr < 0,
                                          len(labels) + objarr, objarr)
                    return objarr

                # this is not the most robust, but...
                if (isinstance(labels, MultiIndex) and
                        not isinstance(objarr[0], tuple)):
                    level = 0
                    _, indexer = labels.reindex(objarr, level=level)

                    check = labels.levels[0].get_indexer(objarr)
                else:
                    level = None

                    # unique index
                    if labels.is_unique:
                        indexer = check = labels.get_indexer(objarr)

                    # non-unique (dups)
                    else:
                        (indexer,
                         missing) = labels.get_indexer_non_unique(objarr)
                        check = indexer

                mask = check == -1
                if mask.any():

                    # mi here
                    if isinstance(obj, tuple) and is_setter:
                        return {'key': obj}
                    raise KeyError('%s not in index' % objarr[mask])

                return indexer

        else:
            try:
                return labels.get_loc(obj)
            except KeyError:
                # allow a not found key only if we are a setter
                if not is_list_like(obj) and is_setter:
                    return {'key': obj}
                raise
