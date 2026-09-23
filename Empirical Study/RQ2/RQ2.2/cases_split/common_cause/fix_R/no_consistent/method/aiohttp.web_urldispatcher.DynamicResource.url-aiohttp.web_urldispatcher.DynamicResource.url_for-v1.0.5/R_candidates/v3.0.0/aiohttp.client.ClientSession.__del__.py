    def __del__(self, _warnings=warnings):
        if not self.closed:
            if PY_36:
                kwargs = {'source': self}
            else:
                kwargs = {}
            _warnings.warn("Unclosed client session {!r}".format(self),
                           ResourceWarning,
                           **kwargs)
            context = {'client_session': self,
                       'message': 'Unclosed client session'}
            if self._source_traceback is not None:
                context['source_traceback'] = self._source_traceback
            self._loop.call_exception_handler(context)
