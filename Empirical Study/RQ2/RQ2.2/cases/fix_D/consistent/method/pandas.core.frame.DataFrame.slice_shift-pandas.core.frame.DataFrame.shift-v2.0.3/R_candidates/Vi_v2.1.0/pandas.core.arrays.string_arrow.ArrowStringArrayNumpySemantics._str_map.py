    def _str_map(
        self, f, na_value=None, dtype: Dtype | None = None, convert: bool = True
    ):
        if dtype is None:
            dtype = self.dtype
        if na_value is None:
            na_value = self.dtype.na_value

        mask = isna(self)
        arr = np.asarray(self)

        if is_integer_dtype(dtype) or is_bool_dtype(dtype):
            if is_integer_dtype(dtype):
                na_value = np.nan
            else:
                na_value = False
            try:
                result = lib.map_infer_mask(
                    arr,
                    f,
                    mask.view("uint8"),
                    convert=False,
                    na_value=na_value,
                    dtype=np.dtype(dtype),  # type: ignore[arg-type]
                )
                return result

            except ValueError:
                result = lib.map_infer_mask(
                    arr,
                    f,
                    mask.view("uint8"),
                    convert=False,
                    na_value=na_value,
                )
                if convert and result.dtype == object:
                    result = lib.maybe_convert_objects(result)
                return result

        elif is_string_dtype(dtype) and not is_object_dtype(dtype):
            # i.e. StringDtype
            result = lib.map_infer_mask(
                arr, f, mask.view("uint8"), convert=False, na_value=na_value
            )
            result = pa.array(result, mask=mask, type=pa.string(), from_pandas=True)
            return type(self)(result)
        else:
            # This is when the result type is object. We reach this when
            # -> We know the result type is truly object (e.g. .encode returns bytes
            #    or .findall returns a list).
            # -> We don't know the result type. E.g. `.get` can return anything.
            return lib.map_infer_mask(arr, f, mask.view("uint8"))
