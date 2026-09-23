    def get_base(self, x):
        y = x
        while y.base is not None:
            y = y.base
        return y
