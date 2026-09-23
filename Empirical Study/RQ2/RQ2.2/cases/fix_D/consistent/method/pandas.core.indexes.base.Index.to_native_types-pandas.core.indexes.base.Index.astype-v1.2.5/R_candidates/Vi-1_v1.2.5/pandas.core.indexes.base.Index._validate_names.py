    @final
    def _validate_names(self, name=None, names=None, deep: bool = False) -> List[Label]:
        """
        Handles the quirks of having a singular 'name' parameter for general
        Index and plural 'names' parameter for MultiIndex.
        """
        from copy import deepcopy

        if names is not None and name is not None:
            raise TypeError("Can only provide one of `names` and `name`")
        elif names is None and name is None:
            new_names = deepcopy(self.names) if deep else self.names
        elif names is not None:
            if not is_list_like(names):
                raise TypeError("Must pass list-like as `names`.")
            new_names = names
        elif not is_list_like(name):
            new_names = [name]
        else:
            new_names = name

        if len(new_names) != len(self.names):
            raise ValueError(
                f"Length of new names must be {len(self.names)}, got {len(new_names)}"
            )

        # All items in 'new_names' need to be hashable
        validate_all_hashable(*new_names, error_name=f"{type(self).__name__}.name")

        return new_names
