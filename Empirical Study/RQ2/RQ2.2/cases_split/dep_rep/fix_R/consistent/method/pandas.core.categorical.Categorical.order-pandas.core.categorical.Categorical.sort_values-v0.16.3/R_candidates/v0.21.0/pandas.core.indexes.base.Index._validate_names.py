    def _validate_names(self, name=None, names=None, deep=False):
        """
        Handles the quirks of having a singular 'name' parameter for general
        Index and plural 'names' parameter for MultiIndex.
        """
        from copy import deepcopy
        if names is not None and name is not None:
            raise TypeError("Can only provide one of `names` and `name`")
        elif names is None and name is None:
            return deepcopy(self.names) if deep else self.names
        elif names is not None:
            if not is_list_like(names):
                raise TypeError("Must pass list-like as `names`.")
            return names
        else:
            if not is_list_like(name):
                return [name]
            return name
