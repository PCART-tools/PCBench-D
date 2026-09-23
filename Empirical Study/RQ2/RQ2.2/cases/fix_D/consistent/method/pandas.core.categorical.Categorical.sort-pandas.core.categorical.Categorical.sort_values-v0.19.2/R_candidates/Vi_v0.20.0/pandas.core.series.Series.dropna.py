    def dropna(self, axis=0, inplace=False, **kwargs):
        """
        Return Series without null values

        Returns
        -------
        valid : Series
        inplace : boolean, default False
            Do operation in place.
        """
        inplace = validate_bool_kwarg(inplace, 'inplace')
        kwargs.pop('how', None)
        if kwargs:
            raise TypeError('dropna() got an unexpected keyword '
                            'argument "{0}"'.format(list(kwargs.keys())[0]))

        axis = self._get_axis_number(axis or 0)

        if self._can_hold_na:
            result = remove_na(self)
            if inplace:
                self._update_inplace(result)
            else:
                return result
        else:
            if inplace:
                # do nothing
                pass
            else:
                return self.copy()
