    @Appender(_shared_docs['find'] %
              dict(side='lowest', method='find',
                   also='rfind : Return highest indexes in each strings'))
    def find(self, sub, start=0, end=None):
        result = str_find(self._data, sub, start=start, end=end, side='left')
        return self._wrap_result(result)
