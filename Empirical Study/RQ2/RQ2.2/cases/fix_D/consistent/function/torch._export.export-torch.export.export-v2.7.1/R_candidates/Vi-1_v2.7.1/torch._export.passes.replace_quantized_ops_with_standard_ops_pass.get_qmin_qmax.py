def get_qmin_qmax(dtype: torch.dtype) -> tuple[Union[int, float], Union[int, float]]:
    return calculate_qmin_qmax(None, None, False, dtype, False)  # type: ignore[arg-type]
