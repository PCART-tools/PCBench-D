    def _send_headers(self, resp_impl):
        # Durty hack required for
        # https://github.com/KeepSafe/aiohttp/issues/1093
        # File sender may override it
        resp_impl.send_headers()
