    def __hash__(self):
        return hash((self._gridspec, self.num1, self.num2))
