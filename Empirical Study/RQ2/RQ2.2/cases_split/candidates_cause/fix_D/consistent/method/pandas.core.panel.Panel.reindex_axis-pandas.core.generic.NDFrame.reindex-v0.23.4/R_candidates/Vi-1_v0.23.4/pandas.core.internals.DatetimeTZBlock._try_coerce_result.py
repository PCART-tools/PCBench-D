    def _try_coerce_result(self, result):
        """ reverse of try_coerce_args """
        if isinstance(result, np.ndarray):
            if result.dtype.kind in ['i', 'f', 'O']:
                result = result.astype('M8[ns]')
        elif isinstance(result, (np.integer, np.float, np.datetime64)):
            result = tslib.Timestamp(result, tz=self.values.tz)
        if isinstance(result, np.ndarray):
            # allow passing of > 1dim if its trivial
            if result.ndim > 1:
                result = result.reshape(np.prod(result.shape))
            result = self.values._shallow_copy(result)

        return result
