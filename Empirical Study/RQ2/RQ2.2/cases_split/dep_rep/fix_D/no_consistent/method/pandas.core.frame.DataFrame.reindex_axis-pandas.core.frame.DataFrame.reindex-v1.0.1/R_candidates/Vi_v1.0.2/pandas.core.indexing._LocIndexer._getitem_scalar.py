    def _getitem_scalar(self, key):
        # a fast-path to scalar access
        # if not, raise
        values = self.obj._get_value(*key)
        return values
