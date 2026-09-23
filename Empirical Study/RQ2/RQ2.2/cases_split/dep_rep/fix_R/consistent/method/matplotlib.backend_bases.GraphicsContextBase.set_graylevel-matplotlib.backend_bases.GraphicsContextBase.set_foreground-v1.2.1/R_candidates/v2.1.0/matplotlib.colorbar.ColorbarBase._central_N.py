    def _central_N(self):
        '''number of boundaries **before** extension of ends'''
        nb = len(self._boundaries)
        if self.extend == 'both':
            nb -= 2
        elif self.extend in ('min', 'max'):
            nb -= 1
        return nb
