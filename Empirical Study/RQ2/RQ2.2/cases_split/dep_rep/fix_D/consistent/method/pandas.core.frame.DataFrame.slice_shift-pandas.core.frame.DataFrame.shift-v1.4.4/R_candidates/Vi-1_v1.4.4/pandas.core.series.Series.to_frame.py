    def to_frame(self, name: Hashable = lib.no_default) -> DataFrame:
        """
        Convert Series to DataFrame.

        Parameters
        ----------
        name : object, optional
            The passed name should substitute for the series name (if it has
            one).

        Returns
        -------
        DataFrame
            DataFrame representation of Series.

        Examples
        --------
        >>> s = pd.Series(["a", "b", "c"],
        ...               name="vals")
        >>> s.to_frame()
          vals
        0    a
        1    b
        2    c
        """
        if name is None:
            warnings.warn(
                "Explicitly passing `name=None` currently preserves the Series' name "
                "or uses a default name of 0. This behaviour is deprecated, and in "
                "the future `None` will be used as the name of the resulting "
                "DataFrame column.",
                FutureWarning,
                stacklevel=find_stack_level(),
            )
            name = lib.no_default

        columns: Index
        if name is lib.no_default:
            name = self.name
            if name is None:
                # default to [0], same as we would get with DataFrame(self)
                columns = default_index(1)
            else:
                columns = Index([name])
        else:
            columns = Index([name])

        mgr = self._mgr.to_2d_mgr(columns)
        return self._constructor_expanddim(mgr)
