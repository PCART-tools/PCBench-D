@lru_cache(256)
def _to_python_date(value: int | float) -> date:
    """Convert polars int64 timestamp to Python date."""
    return (EPOCH_UTC + timedelta(seconds=value * 86400)).date()
