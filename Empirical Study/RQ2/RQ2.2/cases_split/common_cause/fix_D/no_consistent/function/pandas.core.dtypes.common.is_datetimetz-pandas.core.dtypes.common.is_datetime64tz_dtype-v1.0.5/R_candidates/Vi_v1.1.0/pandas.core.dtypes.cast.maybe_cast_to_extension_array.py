def maybe_cast_to_extension_array(cls: Type["ExtensionArray"], obj, dtype=None):
    """
    Call to `_from_sequence` that returns the object unchanged on Exception.

    Parameters
    ----------
    cls : class, subclass of ExtensionArray
    obj : arraylike
        Values to pass to cls._from_sequence
    dtype : ExtensionDtype, optional

    Returns
    -------
    ExtensionArray or obj
    """
    from pandas.core.arrays.string_ import StringArray

    assert isinstance(cls, type), f"must pass a type: {cls}"
    assertion_msg = f"must pass a subclass of ExtensionArray: {cls}"
    assert issubclass(cls, ABCExtensionArray), assertion_msg

    # Everything can be be converted to StringArrays, but we may not want to convert
    if issubclass(cls, StringArray) and lib.infer_dtype(obj) != "string":
        return obj

    try:
        result = cls._from_sequence(obj, dtype=dtype)
    except Exception:
        # We can't predict what downstream EA constructors may raise
        result = obj
    return result
