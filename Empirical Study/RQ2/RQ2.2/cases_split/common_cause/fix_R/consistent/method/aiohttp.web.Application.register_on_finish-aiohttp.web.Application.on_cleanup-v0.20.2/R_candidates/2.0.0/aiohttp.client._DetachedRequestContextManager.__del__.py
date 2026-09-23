    def __del__(self):
        self._session.detach()
