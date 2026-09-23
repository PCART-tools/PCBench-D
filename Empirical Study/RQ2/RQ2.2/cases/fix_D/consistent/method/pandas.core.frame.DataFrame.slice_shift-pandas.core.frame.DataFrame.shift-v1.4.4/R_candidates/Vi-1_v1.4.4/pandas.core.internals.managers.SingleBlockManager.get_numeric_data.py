    def get_numeric_data(self, copy: bool = False):
        if self._block.is_numeric:
            if copy:
                return self.copy()
            return self
        return self.make_empty()
