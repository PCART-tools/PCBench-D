    def is_categorical(self):
        """
        Check if the Index holds categorical data.

        Returns
        -------
        boolean
            True if the Index is categorical.

        See Also
        --------
        CategoricalIndex : Index for categorical data.

        Examples
        --------
        >>> idx = pd.Index(["Watermelon", "Orange", "Apple",
        ...                 "Watermelon"]).astype("category")
        >>> idx.is_categorical()
        True

        >>> idx = pd.Index([1, 3, 5, 7])
        >>> idx.is_categorical()
        False

        >>> s = pd.Series(["Peter", "Victor", "Elisabeth", "Mar"])
        >>> s
        0        Peter
        1       Victor
        2    Elisabeth
        3          Mar
        dtype: object
        >>> s.index.is_categorical()
        False
        """
        return self.inferred_type in ["categorical"]
