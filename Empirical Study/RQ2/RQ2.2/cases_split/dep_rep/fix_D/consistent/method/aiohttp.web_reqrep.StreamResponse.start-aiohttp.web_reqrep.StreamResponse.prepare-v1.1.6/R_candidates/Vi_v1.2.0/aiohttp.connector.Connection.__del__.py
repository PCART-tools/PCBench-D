    def __del__(self, _warnings=warnings):
        if self._transport is not None:
            _warnings.warn('Unclosed connection {!r}'.format(self),
                           ResourceWarning)
            if self._loop.is_closed():
                return

            self._connector._release(
                self._key, self._request, self._transport, self._protocol,
                should_close=True)

            context = {'client_connection': self,
                       'message': 'Unclosed connection'}
            if self._source_traceback is not None:
                context['source_traceback'] = self._source_traceback
            self._loop.call_exception_handler(context)
