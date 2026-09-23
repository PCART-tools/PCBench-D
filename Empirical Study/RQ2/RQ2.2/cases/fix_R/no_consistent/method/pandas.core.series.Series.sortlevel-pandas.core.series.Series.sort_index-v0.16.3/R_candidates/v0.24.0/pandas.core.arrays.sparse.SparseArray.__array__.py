    def __array__(self, dtype=None, copy=True):
        fill_value = self.fill_value

        if self.sp_index.ngaps == 0:
            # Compat for na dtype and int values.
            return self.sp_values
        if dtype is None:
            # Can NumPy represent this type?
            # If not, `np.result_type` will raise. We catch that
            # and return object.
            if is_datetime64_any_dtype(self.sp_values.dtype):
                # However, we *do* special-case the common case of
                # a datetime64 with pandas NaT.
                if fill_value is NaT:
                    # Can't put pd.NaT in a datetime64[ns]
                    fill_value = np.datetime64('NaT')
            try:
                dtype = np.result_type(self.sp_values.dtype, type(fill_value))
            except TypeError:
                dtype = object

        out = np.full(self.shape, fill_value, dtype=dtype)
        out[self.sp_index.to_int_index().indices] = self.sp_values
        return out
