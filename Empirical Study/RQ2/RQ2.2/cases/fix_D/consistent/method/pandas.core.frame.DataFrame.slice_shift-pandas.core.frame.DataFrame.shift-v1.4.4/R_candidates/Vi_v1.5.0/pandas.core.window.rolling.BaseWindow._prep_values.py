    def _prep_values(self, values: ArrayLike) -> np.ndarray:
        """Convert input to numpy arrays for Cython routines"""
        if needs_i8_conversion(values.dtype):
            raise NotImplementedError(
                f"ops for {type(self).__name__} for this "
                f"dtype {values.dtype} are not implemented"
            )
        else:
            # GH #12373 : rolling functions error on float32 data
            # make sure the data is coerced to float64
            try:
                if isinstance(values, ExtensionArray):
                    values = values.to_numpy(np.float64, na_value=np.nan)
                else:
                    values = ensure_float64(values)
            except (ValueError, TypeError) as err:
                raise TypeError(f"cannot handle this type -> {values.dtype}") from err

        # Convert inf to nan for C funcs
        inf = np.isinf(values)
        if inf.any():
            values = np.where(inf, np.nan, values)

        return values
