class TransportError(RequestError):
    """
    Base class for all exceptions that occur at the level of the Transport API.

    All of these exceptions also have an equivelent mapping in `httpcore`.
    """
