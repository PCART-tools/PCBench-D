    def __del__(self, _warnings=warnings):
        if self._loop is None:
            return  # not started
        if self._closed:
            return

        if self._connection is not None:
            self._connection.release()
            self._cleanup_writer()

            # warn
            if __debug__:
                if self._loop.get_debug():
                    _warnings.warn("Unclosed response {!r}".format(self),
                                   ResourceWarning)
                    context = {'client_response': self,
                               'message': 'Unclosed response'}
                    if self._source_traceback:
                        context['source_traceback'] = self._source_traceback
                    self._loop.call_exception_handler(context)
