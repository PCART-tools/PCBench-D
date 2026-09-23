    def _try_coerce_result(self, result):
        """ reverse of try_coerce_args / try_operate """
        if isinstance(result, np.ndarray):
            mask = isnull(result)
            if result.dtype.kind in ['i', 'f', 'O']:
                result = result.astype('m8[ns]')
            result[mask] = tslib.iNaT
        elif isinstance(result, np.integer):
            result = lib.Timedelta(result)
        return result
