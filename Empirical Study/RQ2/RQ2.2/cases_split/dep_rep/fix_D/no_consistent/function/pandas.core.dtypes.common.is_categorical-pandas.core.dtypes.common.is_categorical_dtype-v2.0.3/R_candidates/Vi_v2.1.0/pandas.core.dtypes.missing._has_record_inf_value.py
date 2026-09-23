def _has_record_inf_value(record_as_array: np.ndarray) -> np.bool_:
    is_inf_in_record = np.zeros(len(record_as_array), dtype=bool)
    for i, value in enumerate(record_as_array):
        is_element_inf = False
        try:
            is_element_inf = np.isinf(value)
        except TypeError:
            is_element_inf = False
        is_inf_in_record[i] = is_element_inf

    return np.any(is_inf_in_record)
