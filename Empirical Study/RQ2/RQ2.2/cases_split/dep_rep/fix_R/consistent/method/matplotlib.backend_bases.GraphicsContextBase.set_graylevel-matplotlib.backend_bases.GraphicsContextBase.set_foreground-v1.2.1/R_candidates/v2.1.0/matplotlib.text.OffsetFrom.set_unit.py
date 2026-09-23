    def set_unit(self, unit):
        '''
        The unit for input to the transform used by ``__call__``

        Parameters
        ----------
        unit : {'points', 'pixels'}
        '''
        if unit not in ["points", "pixels"]:
            raise ValueError("'unit' must be one of [ 'points' | 'pixels' ]")
        self._unit = unit
