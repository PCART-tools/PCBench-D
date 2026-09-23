    def __setitem__(self, key, value):
        key = com.apply_if_callable(key, self)
        cacher_needs_updating = self._check_is_chained_assignment_possible()

        try:
            self._set_with_engine(key, value)
        except com.SettingWithCopyError:
            raise
        except (KeyError, ValueError):
            values = self._values
            if is_integer(key) and not self.index.inferred_type == "integer":
                values[key] = value
            elif key is Ellipsis:
                self[:] = value
            else:
                self.loc[key] = value

        except TypeError as e:
            if isinstance(key, tuple) and not isinstance(self.index, MultiIndex):
                raise ValueError("Can only tuple-index with a MultiIndex")

            # python 3 type errors should be raised
            if _is_unorderable_exception(e):
                raise IndexError(key)

            if com.is_bool_indexer(key):
                key = check_bool_indexer(self.index, key)
                try:
                    self._where(~key, value, inplace=True)
                    return
                except InvalidIndexError:
                    pass

            self._set_with(key, value)

        if cacher_needs_updating:
            self._maybe_update_cacher()
