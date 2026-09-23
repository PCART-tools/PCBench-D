    def get_level_values(self, level):
        """
        Return vector of label values for requested level, equal to the length
        of the index

        Parameters
        ----------
        level : int or level name

        Returns
        -------
        values : ndarray
        """
        num = self._get_level_number(level)
        unique = self.levels[num]  # .values
        labels = self.labels[num]
        filled = com.take_1d(unique.values, labels, fill_value=unique._na_value)
        values = unique._simple_new(filled, self.names[num],
                                    freq=getattr(unique, 'freq', None),
                                    tz=getattr(unique, 'tz', None))
        return values
