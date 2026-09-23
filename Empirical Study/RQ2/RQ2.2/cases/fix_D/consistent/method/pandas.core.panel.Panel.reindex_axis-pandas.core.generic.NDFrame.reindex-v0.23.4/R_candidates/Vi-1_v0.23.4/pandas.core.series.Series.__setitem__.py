    def __setitem__(self, key, value):
        key = com._apply_if_callable(key, self)

        def setitem(key, value):
            try:
                self._set_with_engine(key, value)
                return
            except com.SettingWithCopyError:
                raise
            except (KeyError, ValueError):
                values = self._values
                if (is_integer(key) and
                        not self.index.inferred_type == 'integer'):

                    values[key] = value
                    return
                elif key is Ellipsis:
                    self[:] = value
                    return
                elif com.is_bool_indexer(key):
                    pass
                elif is_timedelta64_dtype(self.dtype):
                    # reassign a null value to iNaT
                    if isna(value):
                        value = iNaT

                        try:
                            self.index._engine.set_value(self._values, key,
                                                         value)
                            return
                        except TypeError:
                            pass

                self.loc[key] = value
                return

            except TypeError as e:
                if (isinstance(key, tuple) and
                        not isinstance(self.index, MultiIndex)):
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

        # do the setitem
        cacher_needs_updating = self._check_is_chained_assignment_possible()
        setitem(key, value)
        if cacher_needs_updating:
            self._maybe_update_cacher()
