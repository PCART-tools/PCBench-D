  def runtime_executable(self) -> Any | None:
    """An arbitrary object representation of this executable.

    Intended for debugging purposes. This is not valid nor reliable
    serialization. The output has no guarantee of consistency across
    invocations.

    Returns ``None`` if unavailable, e.g. based on backend, compiler, or
    runtime.
    """
    return self._executable.runtime_executable()
