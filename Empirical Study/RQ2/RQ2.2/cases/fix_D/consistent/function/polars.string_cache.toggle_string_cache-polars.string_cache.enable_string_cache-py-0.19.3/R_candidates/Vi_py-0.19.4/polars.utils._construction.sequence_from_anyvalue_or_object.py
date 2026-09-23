def sequence_from_anyvalue_or_object(name: str, values: Sequence[Any]) -> PySeries:
    """
    Last resort conversion.

    AnyValues are most flexible and if they fail we go for object types

    """
    try:
        return PySeries.new_from_anyvalues(name, values, strict=True)
    # raised if we cannot convert to Wrap<AnyValue>
    except RuntimeError:
        return PySeries.new_object(name, values, _strict=False)
    except ComputeError as exc:
        if "mixed dtypes" in str(exc):
            return PySeries.new_object(name, values, _strict=False)
        raise
