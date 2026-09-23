    def _try_coerce_result(self, result):
        """ reverse of try_coerce_args """
        if isinstance(result, np.ndarray):
            if result.dtype.kind in ['i', 'f']:
                result = result.astype('M8[ns]')

        elif isinstance(result, (np.integer, np.float, np.datetime64)):
            result = self._box_func(result)
        return result
