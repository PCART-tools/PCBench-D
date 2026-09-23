    def _post_setstate(self):
        self._is_consolidated = False
        self._known_consolidated = False
        self._rebuild_blknos_and_blklocs()
