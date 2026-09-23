def _float2str(value: float, precision: Optional[int] = None) -> str:
    return (f"{value:.{precision}f}"
            if precision is not None and not isinstance(value, str)
            else str(value))
