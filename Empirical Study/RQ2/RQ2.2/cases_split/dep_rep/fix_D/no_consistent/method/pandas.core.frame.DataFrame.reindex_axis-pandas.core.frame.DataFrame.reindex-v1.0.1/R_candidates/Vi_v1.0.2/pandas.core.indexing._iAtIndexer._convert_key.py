    def _convert_key(self, key, is_setter: bool = False):
        """
        Require integer args. (and convert to label arguments)
        """
        for a, i in zip(self.obj.axes, key):
            if not is_integer(i):
                raise ValueError("iAt based indexing can only have integer indexers")
        return key
