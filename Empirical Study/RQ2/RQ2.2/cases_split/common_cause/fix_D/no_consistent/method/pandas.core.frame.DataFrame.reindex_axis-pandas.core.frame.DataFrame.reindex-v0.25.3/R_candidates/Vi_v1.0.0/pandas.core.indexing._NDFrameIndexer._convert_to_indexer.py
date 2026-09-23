    def _convert_to_indexer(self, obj, axis: int, raise_missing: bool = False):
        """
        Convert indexing key into something we can use to do actual fancy
        indexing on a ndarray.

        Examples
        ix[:5] -> slice(0, 5)
        ix[[1,2,3]] -> [1,2,3]
        ix[['foo', 'bar', 'baz']] -> [i, j, k] (indices of foo, bar, baz)

        Going by Zen of Python?
        'In the face of ambiguity, refuse the temptation to guess.'
        raise AmbiguousIndexError with integer labels?
        - No, prefer label-based indexing
        """
        labels = self.obj._get_axis(axis)

        if isinstance(obj, slice):
            return self._convert_slice_indexer(obj, axis)

        # try to find out correct indexer, if not type correct raise
        try:
            obj = self._convert_scalar_indexer(obj, axis)
        except TypeError:
            # but we will allow setting
            pass

        # see if we are positional in nature
        is_int_index = labels.is_integer()
        is_int_positional = is_integer(obj) and not is_int_index

        # if we are a label return me
        try:
            return labels.get_loc(obj)
        except LookupError:
            if isinstance(obj, tuple) and isinstance(labels, ABCMultiIndex):
                if len(obj) == labels.nlevels:
                    return {"key": obj}
                raise
        except TypeError:
            pass
        except ValueError:
            if not is_int_positional:
                raise

        # a positional
        if is_int_positional:

            # if we are setting and its not a valid location
            # its an insert which fails by definition

            if self.name == "loc":
                # always valid
                return {"key": obj}

            if obj >= self.obj.shape[axis] and not isinstance(labels, ABCMultiIndex):
                # a positional
                raise ValueError("cannot set by positional indexing with enlargement")

            return obj

        if is_nested_tuple(obj, labels):
            return labels.get_locs(obj)

        elif is_list_like_indexer(obj):

            if com.is_bool_indexer(obj):
                obj = check_bool_indexer(labels, obj)
                (inds,) = obj.nonzero()
                return inds
            else:
                # When setting, missing keys are not allowed, even with .loc:
                return self._get_listlike_indexer(obj, axis, raise_missing=True)[1]
        else:
            try:
                return labels.get_loc(obj)
            except LookupError:
                # allow a not found key only if we are a setter
                if not is_list_like_indexer(obj):
                    return {"key": obj}
                raise
