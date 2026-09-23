    def _consolidate_inplace(self):
        if not self.is_consolidated():
            self.blocks = tuple(_consolidate(self.blocks))
            self._is_consolidated = True
            self._known_consolidated = True
            self._rebuild_blknos_and_blklocs()
