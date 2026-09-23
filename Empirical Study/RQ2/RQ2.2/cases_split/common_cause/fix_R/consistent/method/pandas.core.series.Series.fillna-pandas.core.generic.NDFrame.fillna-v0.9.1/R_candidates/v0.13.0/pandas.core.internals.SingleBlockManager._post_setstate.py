    def _post_setstate(self):
        self._block = self.blocks[0]
        self._values = self._block.values
