    @Appender(_shared_docs['str_strip'] % dict(side='left and right sides',
              method='strip'))
    def strip(self, to_strip=None):
        result = str_strip(self.series, to_strip, side='both')
        return self._wrap_result(result)
