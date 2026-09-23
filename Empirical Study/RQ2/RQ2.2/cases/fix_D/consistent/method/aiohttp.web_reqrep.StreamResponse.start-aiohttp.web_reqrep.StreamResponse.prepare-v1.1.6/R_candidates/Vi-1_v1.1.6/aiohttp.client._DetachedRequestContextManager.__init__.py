    def __init__(self, coro, session):
        super().__init__(coro)
        self._session = session
