    def set_unit(self, unit):
        '''
        The unit for input to the transform used by ``__call__``

        Parameters
        ----------
        unit : {'points', 'pixels'}
        '''
        cbook._check_in_list(["points", "pixels"], unit=unit)
        self._unit = unit
