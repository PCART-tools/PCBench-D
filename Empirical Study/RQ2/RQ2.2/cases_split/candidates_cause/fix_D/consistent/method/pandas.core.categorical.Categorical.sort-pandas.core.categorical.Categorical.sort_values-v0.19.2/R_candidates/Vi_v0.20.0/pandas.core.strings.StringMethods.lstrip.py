    @Appender(_shared_docs['str_strip'] % dict(side='left side',
                                               method='lstrip'))
    def lstrip(self, to_strip=None):
        result = str_strip(self._data, to_strip, side='left')
        return self._wrap_result(result)
