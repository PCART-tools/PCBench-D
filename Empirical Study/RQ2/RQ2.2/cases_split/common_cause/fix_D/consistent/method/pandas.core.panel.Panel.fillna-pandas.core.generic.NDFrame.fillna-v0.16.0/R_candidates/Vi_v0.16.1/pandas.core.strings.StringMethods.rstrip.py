    @Appender(_shared_docs['str_strip'] % dict(side='right side',
              method='rstrip'))
    def rstrip(self, to_strip=None):
        result = str_strip(self.series, to_strip, side='right')
        return self._wrap_result(result)
