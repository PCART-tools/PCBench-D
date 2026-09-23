    @Appender(_shared_docs['find'] % dict(side='highest', method='rfind',
              also='find : Return lowest indexes in each strings'))
    def rfind(self, sub, start=0, end=None):
        result = str_find(self.series, sub, start=start, end=end, side='right')
        return self._wrap_result(result)
