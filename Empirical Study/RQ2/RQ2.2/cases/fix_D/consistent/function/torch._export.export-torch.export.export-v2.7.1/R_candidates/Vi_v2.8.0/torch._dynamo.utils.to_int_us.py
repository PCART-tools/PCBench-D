def to_int_us(v: Optional[float]) -> Optional[int]:
    return None if v is None else int(v * 1_000_000)
