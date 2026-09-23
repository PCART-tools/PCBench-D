    def _box_values(self, values):
        """
        apply box func to passed values
        """
        import pandas.lib as lib
        return lib.map_infer(values, self._box_func)
