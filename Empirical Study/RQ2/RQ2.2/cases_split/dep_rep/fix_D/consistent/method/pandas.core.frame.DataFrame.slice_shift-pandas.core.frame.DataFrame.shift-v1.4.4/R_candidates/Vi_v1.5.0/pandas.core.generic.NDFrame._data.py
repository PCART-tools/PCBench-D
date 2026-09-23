    @final
    @property
    def _data(self):
        # GH#33054 retained because some downstream packages uses this,
        #  e.g. fastparquet
        return self._mgr
