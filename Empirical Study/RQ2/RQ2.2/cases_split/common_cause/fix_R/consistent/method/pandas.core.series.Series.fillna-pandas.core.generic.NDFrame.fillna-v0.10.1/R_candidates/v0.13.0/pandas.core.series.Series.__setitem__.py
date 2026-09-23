    def __setitem__(self, key, value):
        try:
            self._set_with_engine(key, value)
            return
        except (SettingWithCopyError):
            raise
        except (KeyError, ValueError):
            values = self.values
            if (com.is_integer(key)
                    and not self.index.inferred_type == 'integer'):

                values[key] = value
                return
            elif key is Ellipsis:
                self[:] = value
                return
            elif _is_bool_indexer(key):
                pass
            elif com.is_timedelta64_dtype(self.dtype):
                # reassign a null value to iNaT
                if isnull(value):
                    value = tslib.iNaT

                    try:
                        self.index._engine.set_value(self.values, key, value)
                        return
                    except (TypeError):
                        pass

            self.loc[key] = value
            return

        except TypeError as e:
            if isinstance(key, tuple) and not isinstance(self.index,
                                                         MultiIndex):
                raise ValueError("Can only tuple-index with a MultiIndex")

            # python 3 type errors should be raised
            if 'unorderable' in str(e):  # pragma: no cover
                raise IndexError(key)

        if _is_bool_indexer(key):
            key = _check_bool_indexer(self.index, key)
            try:
                self.where(~key, value, inplace=True)
                return
            except (InvalidIndexError):
                pass

        self._set_with(key, value)
