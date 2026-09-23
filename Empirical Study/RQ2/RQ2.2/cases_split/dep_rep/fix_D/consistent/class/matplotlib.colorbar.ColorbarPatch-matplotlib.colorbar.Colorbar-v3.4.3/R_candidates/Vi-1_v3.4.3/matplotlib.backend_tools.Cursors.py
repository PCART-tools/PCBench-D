class Cursors(IntEnum):  # Must subclass int for the macOS backend.
    """Backend-independent cursor types."""
    HAND, POINTER, SELECT_REGION, MOVE, WAIT = range(5)
