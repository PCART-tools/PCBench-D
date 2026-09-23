    def __getitem__(self, key):
        try:
            result = self.index.get_value(self, key)
            if isinstance(result, np.ndarray):
                return self._constructor(result,index=[key]*len(result)).__finalize__(self)
            return result
        except InvalidIndexError:
            pass
        except (KeyError, ValueError):
            if isinstance(key, tuple) and isinstance(self.index, MultiIndex):
                # kludge
                pass
            elif key is Ellipsis:
                return self
            elif _is_bool_indexer(key):
                pass
            else:

                # we can try to coerce the indexer (or this will raise)
                new_key = self.index._convert_scalar_indexer(key)
                if type(new_key) != type(key):
                    return self.__getitem__(new_key)
                raise

        except Exception:
            raise

        if com.is_iterator(key):
            key = list(key)

        if _is_bool_indexer(key):
            key = _check_bool_indexer(self.index, key)

        return self._get_with(key)
