def _get_scale_factor(scale: Optional[float], head_size: int) -> float:
    """Get the scale factor for attention computation."""
    return scale if scale is not None else (1.0 / math.sqrt(head_size))
