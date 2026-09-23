    def transpose(self):
        """Transpose index and columns"""
        return super(DataFrame, self).transpose(1, 0)
