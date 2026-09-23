    def _format_with_header(
        self, header: list[str_t], na_rep: str_t = "NaN"
    ) -> list[str_t]:
        from pandas.io.formats.format import format_array

        values = self._values

        if is_object_dtype(values.dtype):
            values = cast(np.ndarray, values)
            values = lib.maybe_convert_objects(values, safe=True)

            result = [pprint_thing(x, escape_chars=("\t", "\r", "\n")) for x in values]

            # could have nans
            mask = isna(values)
            if mask.any():
                result_arr = np.array(result)
                result_arr[mask] = na_rep
                result = result_arr.tolist()
        else:
            result = trim_front(format_array(values, None, justify="left"))
        return header + result
