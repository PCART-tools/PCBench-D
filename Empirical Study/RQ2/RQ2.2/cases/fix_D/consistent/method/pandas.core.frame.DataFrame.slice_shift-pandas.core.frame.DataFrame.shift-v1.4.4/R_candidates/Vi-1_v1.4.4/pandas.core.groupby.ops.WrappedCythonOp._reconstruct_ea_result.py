    def _reconstruct_ea_result(self, values, res_values):
        """
        Construct an ExtensionArray result from an ndarray result.
        """
        # TODO: allow EAs to override this logic

        if isinstance(
            values.dtype, (BooleanDtype, _IntegerDtype, FloatingDtype, StringDtype)
        ):
            dtype = self._get_result_dtype(values.dtype)
            cls = dtype.construct_array_type()
            return cls._from_sequence(res_values, dtype=dtype)

        elif needs_i8_conversion(values.dtype):
            i8values = res_values.view("i8")
            return type(values)(i8values, dtype=values.dtype)

        raise NotImplementedError
