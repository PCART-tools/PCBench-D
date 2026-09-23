def classes(*klasses) -> Callable:
    """evaluate if the tipo is a subclass of the klasses"""
    return lambda tipo: issubclass(tipo, klasses)
