def _timestamp_in_seconds(dt: datetime) -> int:
    du = dt - EPOCH_UTC
    return du.days * 86400 + du.seconds
