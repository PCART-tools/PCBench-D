def register_lowering(
    aten_fn,
    broadcast=False,
    type_promotion_kind: Optional[
        ELEMENTWISE_TYPE_PROMOTION_KIND
    ] = ELEMENTWISE_TYPE_PROMOTION_KIND.DEFAULT,
    convert_input_to_bool=False,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """
    Shim to support decorator syntax.
    """
    return functools.partial(
        _register_lowering,
        aten_fn,
        broadcast=broadcast,
        type_promotion_kind=type_promotion_kind,
        convert_input_to_bool=convert_input_to_bool,
    )
