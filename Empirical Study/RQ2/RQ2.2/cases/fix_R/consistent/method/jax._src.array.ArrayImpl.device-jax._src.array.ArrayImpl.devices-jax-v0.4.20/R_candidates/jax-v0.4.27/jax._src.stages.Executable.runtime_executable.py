  def runtime_executable(self) -> Any:
    """An arbitrary object representation of this executable.

    Intended for debugging purposes. This need not be a valid nor reliable
    serialization. It is relayed directly to external callers, with no
    guarantee on type, structure, or consistency across invocations.

    May raise ``NotImplementedError`` if unavailable, e.g. based on backend or
    compiler.
    """
    raise NotImplementedError
