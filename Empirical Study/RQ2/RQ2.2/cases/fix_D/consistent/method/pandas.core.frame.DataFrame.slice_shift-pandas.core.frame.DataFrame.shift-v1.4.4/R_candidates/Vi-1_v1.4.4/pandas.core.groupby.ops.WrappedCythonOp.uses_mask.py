    def uses_mask(self) -> bool:
        return self.how in self._MASKED_CYTHON_FUNCTIONS
