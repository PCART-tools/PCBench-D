def is_1d_only_ea_obj(obj: Any) -> bool:
    """
    ExtensionArray that does not support 2D, or more specifically that does
    not use HybridBlock.
    """
    from pandas.core.arrays import (
        DatetimeArray,
        ExtensionArray,
        PeriodArray,
        TimedeltaArray,
    )

    return isinstance(obj, ExtensionArray) and not isinstance(
        obj, (DatetimeArray, TimedeltaArray, PeriodArray)
    )
