    def _set_names(self, values, level=None):
        """
        Set new names on index. Each name has to be a hashable type.

        Parameters
        ----------
        values : str or sequence
            name(s) to set
        level : int, level name, or sequence of int/level names (default None)
            If the index is a MultiIndex (hierarchical), level(s) to set (None
            for all levels).  Otherwise level must be None

        Raises
        ------
        TypeError if each name is not hashable.
        """
        if not is_list_like(values):
            raise ValueError("Names must be a list-like")
        if len(values) != 1:
            raise ValueError("Length of new names must be 1, got %d" % len(values))

        # GH 20527
        # All items in 'name' need to be hashable:
        for name in values:
            if not is_hashable(name):
                raise TypeError(
                    "{}.name must be a hashable type".format(self.__class__.__name__)
                )
        self.name = values[0]
