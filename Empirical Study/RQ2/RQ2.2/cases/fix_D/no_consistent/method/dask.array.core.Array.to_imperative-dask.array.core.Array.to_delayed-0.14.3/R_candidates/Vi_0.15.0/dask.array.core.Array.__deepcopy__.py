    def __deepcopy__(self, memo):
        c = self.copy()
        memo[id(self)] = c
        return c
