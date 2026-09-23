    def dropna(self, axis=0, inplace=False, **kwargs):
        """
        Return Series without null values

        Returns
        -------
        valid : Series
        inplace : boolean, default False
            Do operation in place.
        """
        axis = self._get_axis_number(axis or 0)
        result = remove_na(self)
        if inplace:
            self._update_inplace(result)
        else:
            return result
