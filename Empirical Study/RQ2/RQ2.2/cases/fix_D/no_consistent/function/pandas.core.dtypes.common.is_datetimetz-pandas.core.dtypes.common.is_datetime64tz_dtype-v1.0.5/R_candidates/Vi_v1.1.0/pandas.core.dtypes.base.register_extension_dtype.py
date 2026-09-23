def register_extension_dtype(cls: Type[ExtensionDtype]) -> Type[ExtensionDtype]:
    """
    Register an ExtensionType with pandas as class decorator.

    .. versionadded:: 0.24.0

    This enables operations like ``.astype(name)`` for the name
    of the ExtensionDtype.

    Returns
    -------
    callable
        A class decorator.

    Examples
    --------
    >>> from pandas.api.extensions import register_extension_dtype
    >>> from pandas.api.extensions import ExtensionDtype
    >>> @register_extension_dtype
    ... class MyExtensionDtype(ExtensionDtype):
    ...     name = "myextension"
    """
    registry.register(cls)
    return cls
