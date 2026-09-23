    def _find_block(self, item):
        self._check_have(item)
        for i, block in enumerate(self.blocks):
            if item in block:
                return i, block
