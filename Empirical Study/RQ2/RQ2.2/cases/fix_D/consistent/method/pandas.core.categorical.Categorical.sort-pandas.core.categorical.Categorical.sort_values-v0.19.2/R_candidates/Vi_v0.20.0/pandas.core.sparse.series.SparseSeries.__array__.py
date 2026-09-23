    def __array__(self, result=None):
        """ the array interface, return my values """
        return self.block.values
