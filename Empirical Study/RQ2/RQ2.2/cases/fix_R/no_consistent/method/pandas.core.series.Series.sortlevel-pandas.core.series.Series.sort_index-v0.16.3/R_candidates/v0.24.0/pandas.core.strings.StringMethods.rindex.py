    @Appender(_shared_docs['index'] %
              dict(side='highest', similar='rfind', method='rindex',
                   also='index : Return lowest indexes in each strings.'))
    def rindex(self, sub, start=0, end=None):
        result = str_index(self._parent, sub,
                           start=start, end=end, side='right')
        return self._wrap_result(result)
