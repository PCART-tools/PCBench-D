    def _post_setstate(self):
        self._is_consolidated = False
        self._known_consolidated = False
        self._set_has_sparse()
