def _isna_recarray_dtype(values: np.recarray, inf_as_na: bool) -> npt.NDArray[np.bool_]:
    result = np.zeros(values.shape, dtype=bool)
    for i, record in enumerate(values):
        record_as_array = np.array(record.tolist())
        does_record_contain_nan = isna_all(record_as_array)
        does_record_contain_inf = False
        if inf_as_na:
            does_record_contain_inf = bool(_has_record_inf_value(record_as_array))
        result[i] = np.any(
            np.logical_or(does_record_contain_nan, does_record_contain_inf)
        )

    return result
