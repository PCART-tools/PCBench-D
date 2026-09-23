    def __init__(self, coro, session):
        self._coro = coro
        self._resp = None
        self._session = session
