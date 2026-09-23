    def _try_coerce_result(self, result):
        """ reverse of try_coerce_args """
        if isinstance(result, np.ndarray):
            if result.dtype.kind in ['i', 'f', 'O']:
                result = result.astype('M8[ns]')
        elif isinstance(result, (np.integer, np.datetime64)):
            result = lib.Timestamp(result)
        return result
