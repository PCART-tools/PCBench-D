    def get_loc(self, key):
        """
        Get integer location slice for requested label or tuple

        Parameters
        ----------
        key : label or tuple

        Returns
        -------
        loc : int or slice object
        """
        if isinstance(key, tuple):
            if len(key) == self.nlevels:
                if self.is_unique:
                    return self._engine.get_loc(_values_from_object(key))
                else:
                    return slice(*self.slice_locs(key, key))
            else:
                # partial selection
                result = slice(*self.slice_locs(key, key))
                if result.start == result.stop:
                    raise KeyError(key)
                return result
        else:
            return self._get_level_indexer(key, level=0)
