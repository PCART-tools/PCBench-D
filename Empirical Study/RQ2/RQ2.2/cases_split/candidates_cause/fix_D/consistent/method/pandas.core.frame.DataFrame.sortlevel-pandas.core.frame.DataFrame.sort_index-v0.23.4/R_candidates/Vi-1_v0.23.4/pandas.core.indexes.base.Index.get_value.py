    def get_value(self, series, key):
        """
        Fast lookup of value from 1-dimensional ndarray. Only use this if you
        know what you're doing
        """

        # if we have something that is Index-like, then
        # use this, e.g. DatetimeIndex
        s = getattr(series, '_values', None)
        if isinstance(s, (ExtensionArray, Index)) and is_scalar(key):
            # GH 20825
            # Unify Index and ExtensionArray treatment
            # First try to convert the key to a location
            # If that fails, see if key is an integer, and
            # try that
            try:
                iloc = self.get_loc(key)
                return s[iloc]
            except KeyError:
                if is_integer(key):
                    return s[key]

        s = com._values_from_object(series)
        k = com._values_from_object(key)

        k = self._convert_scalar_indexer(k, kind='getitem')
        try:
            return self._engine.get_value(s, k,
                                          tz=getattr(series.dtype, 'tz', None))
        except KeyError as e1:
            if len(self) > 0 and self.inferred_type in ['integer', 'boolean']:
                raise

            try:
                return libindex.get_value_box(s, key)
            except IndexError:
                raise
            except TypeError:
                # generator/iterator-like
                if is_iterator(key):
                    raise InvalidIndexError(key)
                else:
                    raise e1
            except Exception:  # pragma: no cover
                raise e1
        except TypeError:
            # python 3
            if is_scalar(key):  # pragma: no cover
                raise IndexError(key)
            raise InvalidIndexError(key)
