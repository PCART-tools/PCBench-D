    def __array__(self, *args, **kwargs):
        # optimises the access of the transform matrix vs the superclass
        return self.get_matrix()
