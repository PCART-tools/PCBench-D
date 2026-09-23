    def get_numeric_data(self, copy: bool = False):
        if self._block.is_numeric:
            return self.copy(deep=copy)
        return self.make_empty()
