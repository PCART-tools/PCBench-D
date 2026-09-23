def _attribute_type_compatible_with_arg(
    attr: _schemas.AttributeParameter,
    value: ir.Value | int | float | bool | Sequence[int] | Sequence[float] | None,
) -> bool:
    """Check if the attribute type is compatible with the argument."""
    if isinstance(value, bool):
        return attr.type is ir.AttributeType.INT
    if isinstance(value, str):
        return attr.type is ir.AttributeType.STRING
    if isinstance(value, int):
        return attr.type in {ir.AttributeType.INT, ir.AttributeType.FLOAT}
    if isinstance(value, float):
        return attr.type is ir.AttributeType.FLOAT
    if isinstance(value, complex):
        return False
    if isinstance(value, Sequence):
        if attr.type is ir.AttributeType.INTS:
            return all(isinstance(i, int) for i in value)
        if attr.type is ir.AttributeType.FLOATS:
            return all(isinstance(i, (int, float)) for i in value)
    if isinstance(value, torch.dtype):
        return attr.type is ir.AttributeType.INT
    if isinstance(value, (torch.device, torch.memory_format, torch.layout)):
        return attr.type is ir.AttributeType.STRING
    if value is None and not attr.required:
        # An optional attribute is not supplied
        return True
    return False
