class ExecutableNotFoundError(FileNotFoundError):
    """
    Error raised when an executable that Matplotlib optionally
    depends on can't be found.
    """
    pass
