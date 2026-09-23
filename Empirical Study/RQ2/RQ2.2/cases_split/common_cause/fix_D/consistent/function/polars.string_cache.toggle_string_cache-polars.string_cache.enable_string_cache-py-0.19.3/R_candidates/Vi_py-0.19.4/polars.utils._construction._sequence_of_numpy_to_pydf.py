def _sequence_of_numpy_to_pydf(
    first_element: np.ndarray[Any, Any],
    **kwargs: Any,
) -> PyDataFrame:
    to_pydf = (
        _sequence_of_sequence_to_pydf
        if first_element.ndim == 1
        else _sequence_of_elements_to_pydf
    )
    return to_pydf(first_element, **kwargs)  # type: ignore[operator]
