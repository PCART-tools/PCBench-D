    def __del__(self, _warnings=warnings):
        if self._closed:
            return
        if not self._conns:
            return

        conns = [repr(c) for c in self._conns.values()]

        self.close()

        _warnings.warn("Unclosed connector {!r}".format(self),
                       ResourceWarning)
        context = {'connector': self,
                   'connections': conns,
                   'message': 'Unclosed connector'}
        if self._source_traceback is not None:
            context['source_traceback'] = self._source_traceback
        self._loop.call_exception_handler(context)
