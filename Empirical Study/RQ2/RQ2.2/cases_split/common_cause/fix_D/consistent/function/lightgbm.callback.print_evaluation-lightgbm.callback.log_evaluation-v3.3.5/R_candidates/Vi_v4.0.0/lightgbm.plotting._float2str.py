def _float2str(value: float, precision: Optional[int]) -> str:
    return (f"{value:.{precision}f}"
            if precision is not None and not isinstance(value, str)
            else str(value))
