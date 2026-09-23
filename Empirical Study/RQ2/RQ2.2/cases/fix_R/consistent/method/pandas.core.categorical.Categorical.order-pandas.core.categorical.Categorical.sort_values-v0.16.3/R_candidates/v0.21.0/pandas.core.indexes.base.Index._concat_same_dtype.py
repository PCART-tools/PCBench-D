    def _concat_same_dtype(self, to_concat, name):
        """
        Concatenate to_concat which has the same class
        """
        # must be overrided in specific classes
        return _concat._concat_index_asobject(to_concat, name)
