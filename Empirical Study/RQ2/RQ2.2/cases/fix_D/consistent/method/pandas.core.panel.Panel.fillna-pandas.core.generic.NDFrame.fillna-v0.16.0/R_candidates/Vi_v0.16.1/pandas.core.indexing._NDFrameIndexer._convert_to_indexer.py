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
        is_int_positional = is_integer(obj) and not is_int_index

        # if we are a label return me
        try:
            return labels.get_loc(obj)
        except KeyError:
            if isinstance(obj, tuple) and isinstance(labels, MultiIndex):
                if is_setter and len(obj) == labels.nlevels:
                    return {'key': obj}
                raise
        except TypeError:
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
                if (obj >= self.obj.shape[axis] and
                        not isinstance(labels, MultiIndex)):
                    raise ValueError("cannot set by positional indexing with "
                                     "enlargement")

            return obj

        if isinstance(obj, slice):
            return self._convert_slice_indexer(obj, axis)

        elif is_nested_tuple(obj, labels):
            return labels.get_locs(obj)
        elif is_list_like_indexer(obj):
            if is_bool_indexer(obj):
                obj = check_bool_indexer(labels, obj)
                inds, = obj.nonzero()
                return inds
            else:
                if isinstance(obj, Index):
                    objarr = obj.values
                else:
                    objarr = _asarray_tuplesafe(obj)

                # The index may want to handle a list indexer differently
                # by returning an indexer or raising
                indexer = labels._convert_list_indexer(objarr, kind=self.name)
                if indexer is not None:
                    return indexer

                # this is not the most robust, but...
                if (isinstance(labels, MultiIndex) and
                        not isinstance(objarr[0], tuple)):
                    level = 0
                    _, indexer = labels.reindex(objarr, level=level)

                    # take all
                    if indexer is None:
                        indexer = np.arange(len(labels))

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
                    raise KeyError('%s not in index' % objarr[mask])

                return _values_from_object(indexer)

        else:
            try:
                return labels.get_loc(obj)
            except KeyError:
                # allow a not found key only if we are a setter
                if not is_list_like_indexer(obj) and is_setter:
                    return {'key': obj}
                raise
