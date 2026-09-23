    def _convert_key(self, key):
        """
        Require integer args. (and convert to label arguments)
        """
        for i in key:
            if not is_integer(i):
                raise ValueError("iAt based indexing can only have integer indexers")
        return key
