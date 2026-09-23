    def on_eof(self, callback):
        try:
            callback()
        except Exception:
            internal_logger.exception('Exception in eof callback')
