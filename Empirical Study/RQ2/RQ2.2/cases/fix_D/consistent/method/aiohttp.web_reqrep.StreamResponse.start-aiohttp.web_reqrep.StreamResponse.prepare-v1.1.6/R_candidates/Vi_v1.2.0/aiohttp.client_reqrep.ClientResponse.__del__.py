    def __del__(self, _warnings=warnings):
        if self._loop is None:
            return  # not started
        if self._closed:
            return
        self.close()

        _warnings.warn("Unclosed response {!r}".format(self),
                       ResourceWarning)
        context = {'client_response': self,
                   'message': 'Unclosed response'}
        if self._source_traceback:
            context['source_traceback'] = self._source_traceback
        self._loop.call_exception_handler(context)
