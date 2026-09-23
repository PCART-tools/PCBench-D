    @cache_readonly
    def _isnan(self):
        """ return if each value is nan"""
        return self._data.codes == -1
