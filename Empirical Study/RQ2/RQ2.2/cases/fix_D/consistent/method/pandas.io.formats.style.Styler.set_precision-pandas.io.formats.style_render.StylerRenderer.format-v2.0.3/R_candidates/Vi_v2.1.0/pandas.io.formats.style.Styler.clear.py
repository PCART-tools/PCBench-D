    def clear(self) -> None:
        """
        Reset the ``Styler``, removing any previously applied styles.

        Returns None.

        Examples
        --------
        >>> df = pd.DataFrame({'A': [1, 2], 'B': [3, np.nan]})

        After any added style:

        >>> df.style.highlight_null(color='yellow')  # doctest: +SKIP

        Remove it with:

        >>> df.style.clear()  # doctest: +SKIP

        Please see:
        `Table Visualization <../../user_guide/style.ipynb>`_ for more examples.
        """
        # create default GH 40675
        clean_copy = Styler(self.data, uuid=self.uuid)
        clean_attrs = [a for a in clean_copy.__dict__ if not callable(a)]
        self_attrs = [a for a in self.__dict__ if not callable(a)]  # maybe more attrs
        for attr in clean_attrs:
            setattr(self, attr, getattr(clean_copy, attr))
        for attr in set(self_attrs).difference(clean_attrs):
            delattr(self, attr)
