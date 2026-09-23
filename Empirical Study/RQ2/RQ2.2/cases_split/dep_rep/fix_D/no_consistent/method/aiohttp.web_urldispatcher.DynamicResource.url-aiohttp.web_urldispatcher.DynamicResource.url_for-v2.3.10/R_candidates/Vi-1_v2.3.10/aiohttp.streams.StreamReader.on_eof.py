    def on_eof(self, callback):
        if self._eof:
            try:
                callback()
            except Exception:
                internal_logger.exception('Exception in eof callback')
        else:
            self._eof_callbacks.append(callback)
