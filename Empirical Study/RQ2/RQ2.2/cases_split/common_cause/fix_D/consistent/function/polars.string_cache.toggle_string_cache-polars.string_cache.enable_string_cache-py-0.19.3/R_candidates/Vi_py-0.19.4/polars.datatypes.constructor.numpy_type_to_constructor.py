def numpy_type_to_constructor(dtype: type[np.dtype[Any]]) -> Callable[..., PySeries]:
    """Get the right PySeries constructor for the given Polars dtype."""
    if _NUMPY_TYPE_TO_CONSTRUCTOR is None:
        _set_numpy_to_constructor()
    try:
        return _NUMPY_TYPE_TO_CONSTRUCTOR[dtype]  # type:ignore[index]
    except KeyError:
        return PySeries.new_object
    except NameError:  # pragma: no cover
        raise ModuleNotFoundError(
            f"'numpy' is required to convert numpy dtype {dtype!r}"
        ) from None
