    def _format_with_header(self, header, na_rep='NaN', **kwargs):
        values = self.values

        from pandas.core.format import format_array

        if is_categorical_dtype(values.dtype):
            values = np.array(values)
        elif is_object_dtype(values.dtype):
            values = lib.maybe_convert_objects(values, safe=1)

        if is_object_dtype(values.dtype):
            result = [com.pprint_thing(x, escape_chars=('\t', '\r', '\n'))
                      for x in values]

            # could have nans
            mask = isnull(values)
            if mask.any():
                result = np.array(result)
                result[mask] = na_rep
                result = result.tolist()

        else:
            result = _trim_front(format_array(values, None, justify='left'))
        return header + result
