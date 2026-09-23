def record(event: Event, destination: str = "null") -> None:
    _get_or_create_logger(destination).info(event.serialize())
