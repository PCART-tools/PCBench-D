    def _try_coerce_result(self, result):
        """ reverse of try_coerce_args / try_operate """
        if isinstance(result, np.ndarray):
            mask = isna(result)
            if result.dtype.kind in ["i", "f"]:
                result = result.astype("m8[ns]")
            result[mask] = tslibs.iNaT

        elif isinstance(result, (np.integer, np.float)):
            result = self._box_func(result)

        return result
