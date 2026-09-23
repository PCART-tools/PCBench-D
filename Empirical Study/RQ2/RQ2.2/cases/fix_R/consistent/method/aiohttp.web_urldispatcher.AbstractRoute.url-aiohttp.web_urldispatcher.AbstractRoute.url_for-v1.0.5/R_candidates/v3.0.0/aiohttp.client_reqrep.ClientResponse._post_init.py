    def _post_init(self, loop, session):
        self._loop = loop
        self._session = session  # store a reference to session #1985
        if loop.get_debug():
            self._source_traceback = traceback.extract_stack(sys._getframe(1))
