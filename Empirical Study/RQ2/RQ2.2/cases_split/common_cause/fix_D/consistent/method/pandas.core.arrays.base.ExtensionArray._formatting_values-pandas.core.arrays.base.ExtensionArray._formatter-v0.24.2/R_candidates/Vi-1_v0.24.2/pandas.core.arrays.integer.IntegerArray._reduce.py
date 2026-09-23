    def _reduce(self, name, skipna=True, **kwargs):
        data = self._data
        mask = self._mask

        # coerce to a nan-aware float if needed
        if mask.any():
            data = self._data.astype('float64')
            data[mask] = self._na_value

        op = getattr(nanops, 'nan' + name)
        result = op(data, axis=0, skipna=skipna, mask=mask)

        # if we have a boolean op, don't coerce
        if name in ['any', 'all']:
            pass

        # if we have a preservable numeric op,
        # provide coercion back to an integer type if possible
        elif name in ['sum', 'min', 'max', 'prod'] and notna(result):
            int_result = int(result)
            if int_result == result:
                result = int_result

        return result
