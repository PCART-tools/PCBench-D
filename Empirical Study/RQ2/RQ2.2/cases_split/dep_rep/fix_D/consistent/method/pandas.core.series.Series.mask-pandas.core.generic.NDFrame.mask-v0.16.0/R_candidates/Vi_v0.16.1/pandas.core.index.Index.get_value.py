    def get_value(self, series, key):
        """
        Fast lookup of value from 1-dimensional ndarray. Only use this if you
        know what you're doing
        """
        s = _values_from_object(series)
        k = _values_from_object(key)

        # prevent integer truncation bug in indexing
        if is_float(k) and not self.is_floating():
            raise KeyError

        try:
            return self._engine.get_value(s, k)
        except KeyError as e1:
            if len(self) > 0 and self.inferred_type in ['integer','boolean']:
                raise

            try:
                return tslib.get_value_box(s, key)
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
            if np.isscalar(key):  # pragma: no cover
                raise IndexError(key)
            raise InvalidIndexError(key)
