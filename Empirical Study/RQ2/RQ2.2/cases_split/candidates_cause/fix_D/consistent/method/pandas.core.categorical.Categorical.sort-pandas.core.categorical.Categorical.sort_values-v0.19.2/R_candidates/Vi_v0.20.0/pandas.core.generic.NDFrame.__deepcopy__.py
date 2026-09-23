    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}
        return self.copy(deep=True)
