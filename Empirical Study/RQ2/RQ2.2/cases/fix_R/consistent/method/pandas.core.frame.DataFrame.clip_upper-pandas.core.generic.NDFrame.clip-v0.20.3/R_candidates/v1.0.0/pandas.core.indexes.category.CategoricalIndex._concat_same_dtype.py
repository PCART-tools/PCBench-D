    def _concat_same_dtype(self, to_concat, name):
        """
        Concatenate to_concat which has the same class
        ValueError if other is not in the categories
        """
        codes = np.concatenate([self._is_dtype_compat(c).codes for c in to_concat])
        result = self._create_from_codes(codes, name=name)
        # if name is None, _create_from_codes sets self.name
        result.name = name
        return result
