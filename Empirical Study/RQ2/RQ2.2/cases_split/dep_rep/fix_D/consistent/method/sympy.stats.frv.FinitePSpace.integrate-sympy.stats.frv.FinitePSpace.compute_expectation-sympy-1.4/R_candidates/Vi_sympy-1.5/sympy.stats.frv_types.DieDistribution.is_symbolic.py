    @property
    def is_symbolic(self):
        return not self.sides.is_number
