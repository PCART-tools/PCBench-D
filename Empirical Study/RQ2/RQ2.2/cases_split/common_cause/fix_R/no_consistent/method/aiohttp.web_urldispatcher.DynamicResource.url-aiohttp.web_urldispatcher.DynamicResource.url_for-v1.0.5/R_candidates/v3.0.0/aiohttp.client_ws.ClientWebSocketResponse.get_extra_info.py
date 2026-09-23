    def get_extra_info(self, name, default=None):
        """extra info from connection transport"""
        try:
            return self._response.connection.transport.get_extra_info(
                name, default)
        except Exception:
            return default
