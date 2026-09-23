    def unique(self) -> Series:
        """
        Return unique values for each group.

        It returns unique values for each of the grouped values. Returned in
        order of appearance. Hash table-based unique, therefore does NOT sort.

        Returns
        -------
        Series
            Unique values for each of the grouped values.

        See Also
        --------
        Series.unique : Return unique values of Series object.

        Examples
        --------
        >>> df = pd.DataFrame([('Chihuahua', 'dog', 6.1),
        ...                    ('Beagle', 'dog', 15.2),
        ...                    ('Chihuahua', 'dog', 6.9),
        ...                    ('Persian', 'cat', 9.2),
        ...                    ('Chihuahua', 'dog', 7),
        ...                    ('Persian', 'cat', 8.8)],
        ...                   columns=['breed', 'animal', 'height_in'])
        >>> df
               breed     animal   height_in
        0  Chihuahua        dog         6.1
        1     Beagle        dog        15.2
        2  Chihuahua        dog         6.9
        3    Persian        cat         9.2
        4  Chihuahua        dog         7.0
        5    Persian        cat         8.8
        >>> ser = df.groupby('animal')['breed'].unique()
        >>> ser
        animal
        cat              [Persian]
        dog    [Chihuahua, Beagle]
        Name: breed, dtype: object
        """
        result = self._op_via_apply("unique")
        return result
