    def _join_compat(self, other, on=None, how='left', lsuffix='', rsuffix='',
                     sort=False):
        if on is not None:
            raise NotImplementedError("'on' keyword parameter is not yet "
                                      "implemented")
        return self._join_index(other, how, lsuffix, rsuffix)
