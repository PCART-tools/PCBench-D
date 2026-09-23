    def rename(self, mapper, axis, copy=False):
        """ generic rename """

        if axis == 0:
            return self.rename_items(mapper, copy=copy)
        return self.rename_axis(mapper, axis=axis)
