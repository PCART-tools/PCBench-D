    @property
    def is_view(self):
        """ return a boolean if I am possibly a view """
        # check the ndarray values of the DatetimeIndex values
        return self.values.values.base is not None
