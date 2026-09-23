    def _append_same_dtype(self, to_concat, name):
        """
        Concatenate to_concat which has the same class
        ValueError if other is not in the categories
        """
        to_concat = [self._is_dtype_compat(c) for c in to_concat]
        codes = np.concatenate([c.codes for c in to_concat])
        result = self._create_from_codes(codes, name=name)
        # if name is None, _create_from_codes sets self.name
        result.name = name
        return result
