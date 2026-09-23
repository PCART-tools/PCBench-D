    def __getitem__(self, key):
        key = com.apply_if_callable(key, self)
        try:
            result = self.index.get_value(self, key)

            if not is_scalar(result):
                if is_list_like(result) and not isinstance(result, Series):

                    # we need to box if loc of the key isn't scalar here
                    # otherwise have inline ndarray/lists
                    try:
                        if not is_scalar(self.index.get_loc(key)):
                            result = self._constructor(
                                result, index=[key] * len(result), dtype=self.dtype
                            ).__finalize__(self)
                    except KeyError:
                        pass
            return result
        except InvalidIndexError:
            pass
        except (KeyError, ValueError):
            if isinstance(key, tuple) and isinstance(self.index, MultiIndex):
                # kludge
                pass
            elif key is Ellipsis:
                return self
            elif com.is_bool_indexer(key):
                pass
            else:

                # we can try to coerce the indexer (or this will raise)
                new_key = self.index._convert_scalar_indexer(key, kind="getitem")
                if type(new_key) != type(key):
                    return self.__getitem__(new_key)
                raise

        if is_iterator(key):
            key = list(key)

        if com.is_bool_indexer(key):
            key = check_bool_indexer(self.index, key)

        return self._get_with(key)
