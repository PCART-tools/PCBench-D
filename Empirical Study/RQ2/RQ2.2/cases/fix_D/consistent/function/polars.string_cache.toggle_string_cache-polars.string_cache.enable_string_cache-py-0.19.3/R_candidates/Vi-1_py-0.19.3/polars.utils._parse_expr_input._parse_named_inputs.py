def _parse_named_inputs(
    named_inputs: dict[str, IntoExpr], *, structify: bool = False
) -> Iterable[PyExpr]:
    return (
        parse_as_expression(input, structify=structify).alias(name)
        for name, input in named_inputs.items()
    )
