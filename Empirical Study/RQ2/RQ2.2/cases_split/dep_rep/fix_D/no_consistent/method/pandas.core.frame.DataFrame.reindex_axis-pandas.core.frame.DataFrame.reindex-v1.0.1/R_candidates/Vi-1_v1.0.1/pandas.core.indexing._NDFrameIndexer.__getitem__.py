    def __getitem__(self, key):
        # Used in ix and downstream in geopandas _CoordinateIndexer
        if type(key) is tuple:
            # Note: we check the type exactly instead of with isinstance
            #  because NamedTuple is checked separately.
            key = tuple(com.apply_if_callable(x, self.obj) for x in key)
            try:
                values = self.obj._get_value(*key)
            except (KeyError, TypeError, InvalidIndexError, AttributeError):
                # TypeError occurs here if the key has non-hashable entries,
                #  generally slice or list.
                # TODO(ix): most/all of the TypeError cases here are for ix,
                #  so this check can be removed once ix is removed.
                # The InvalidIndexError is only catched for compatibility
                #  with geopandas, see
                #  https://github.com/pandas-dev/pandas/issues/27258
                # TODO: The AttributeError is for IntervalIndex which
                #  incorrectly implements get_value, see
                #  https://github.com/pandas-dev/pandas/issues/27865
                pass
            else:
                if is_scalar(values):
                    return values

            return self._getitem_tuple(key)
        else:
            # we by definition only have the 0th axis
            axis = self.axis or 0

            key = com.apply_if_callable(key, self.obj)
            return self._getitem_axis(key, axis=axis)
