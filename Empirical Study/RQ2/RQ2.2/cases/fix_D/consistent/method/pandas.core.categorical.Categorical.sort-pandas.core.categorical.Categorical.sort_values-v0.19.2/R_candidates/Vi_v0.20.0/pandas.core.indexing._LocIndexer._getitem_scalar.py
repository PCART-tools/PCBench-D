    def _getitem_scalar(self, key):
        # a fast-path to scalar access
        # if not, raise
        values = self.obj.get_value(*key)
        return values
