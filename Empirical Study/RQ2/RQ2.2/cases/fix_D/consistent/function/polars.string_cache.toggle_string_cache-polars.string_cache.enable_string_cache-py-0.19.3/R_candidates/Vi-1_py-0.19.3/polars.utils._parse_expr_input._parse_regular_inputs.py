def _parse_regular_inputs(
    inputs: tuple[IntoExpr | Iterable[IntoExpr], ...],
    *,
    structify: bool = False,
) -> list[PyExpr]:
    if not inputs:
        return []

    inputs_iter: Iterable[IntoExpr]
    if len(inputs) == 1 and _is_iterable(inputs[0]):
        inputs_iter = inputs[0]  # type: ignore[assignment]
    else:
        inputs_iter = inputs  # type: ignore[assignment]

    return [parse_as_expression(e, structify=structify) for e in inputs_iter]
