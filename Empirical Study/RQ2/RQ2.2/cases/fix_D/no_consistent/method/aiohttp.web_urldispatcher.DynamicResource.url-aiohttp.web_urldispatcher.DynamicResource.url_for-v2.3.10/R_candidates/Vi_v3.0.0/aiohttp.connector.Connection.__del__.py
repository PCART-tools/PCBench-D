    def __del__(self, _warnings=warnings):
        if self._protocol is not None:
            if PY_36:
                kwargs = {'source': self}
            else:
                kwargs = {}
            _warnings.warn('Unclosed connection {!r}'.format(self),
                           ResourceWarning,
                           **kwargs)
            if self._loop.is_closed():
                return

            self._connector._release(
                self._key, self._protocol, should_close=True)

            context = {'client_connection': self,
                       'message': 'Unclosed connection'}
            if self._source_traceback is not None:
                context['source_traceback'] = self._source_traceback
            self._loop.call_exception_handler(context)
