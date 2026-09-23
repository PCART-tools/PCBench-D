    def _box_values(self, values) -> np.ndarray:
        """
        apply box func to passed values
        """
        return lib.map_infer(values, self._box_func, convert=False)
