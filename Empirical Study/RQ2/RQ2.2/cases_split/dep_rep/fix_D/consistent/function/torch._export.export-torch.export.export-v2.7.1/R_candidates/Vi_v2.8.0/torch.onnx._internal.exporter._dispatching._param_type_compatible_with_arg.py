def _param_type_compatible_with_arg(
    param: _schemas.Parameter,
    value: ir.TypeProtocol
    | str
    | int
    | float
    | complex
    | Sequence[int]
    | Sequence[float]
    | None,
    assigned_types: dict[str, ir.TypeProtocol],
) -> bool:
    # Handle Python types first
    if isinstance(value, bool):  # noqa: SIM102
        if param.type_constraint.allowed_types & {ir.TensorType(ir.DataType.BOOL)}:
            return True
    if isinstance(value, int) and param.type_constraint.allowed_types & {
        ir.TensorType(ir.DataType.INT4),
        ir.TensorType(ir.DataType.INT8),
        ir.TensorType(ir.DataType.INT16),
        ir.TensorType(ir.DataType.INT32),
        ir.TensorType(ir.DataType.INT64),
        # Int inputs can be casted to a float too
        ir.TensorType(ir.DataType.FLOAT4E2M1),
        ir.TensorType(ir.DataType.FLOAT8E4M3FN),
        ir.TensorType(ir.DataType.FLOAT8E4M3FNUZ),
        ir.TensorType(ir.DataType.FLOAT8E5M2),
        ir.TensorType(ir.DataType.FLOAT8E5M2FNUZ),
        ir.TensorType(ir.DataType.FLOAT16),
        ir.TensorType(ir.DataType.FLOAT),
        ir.TensorType(ir.DataType.DOUBLE),
    }:
        return True
    if isinstance(value, float) and param.type_constraint.allowed_types & {
        ir.TensorType(ir.DataType.FLOAT4E2M1),
        ir.TensorType(ir.DataType.FLOAT8E4M3FN),
        ir.TensorType(ir.DataType.FLOAT8E4M3FNUZ),
        ir.TensorType(ir.DataType.FLOAT8E5M2),
        ir.TensorType(ir.DataType.FLOAT8E5M2FNUZ),
        ir.TensorType(ir.DataType.FLOAT16),
        ir.TensorType(ir.DataType.FLOAT),
        ir.TensorType(ir.DataType.DOUBLE),
    }:
        return True
    if isinstance(value, complex) and param.type_constraint.allowed_types & {
        ir.TensorType(ir.DataType.FLOAT),
        ir.TensorType(ir.DataType.DOUBLE),
        ir.TensorType(ir.DataType.COMPLEX64),
        ir.TensorType(ir.DataType.COMPLEX128),
    }:
        return True
    if isinstance(value, str):  # noqa: SIM102
        if param.type_constraint.allowed_types & {ir.TensorType(ir.DataType.STRING)}:
            return True
    if isinstance(value, (list, tuple)):
        if param.type_constraint.allowed_types & {
            ir.TensorType(ir.DataType.INT32),
            ir.TensorType(ir.DataType.INT64),
            ir.TensorType(ir.DataType.FLOAT),
            ir.TensorType(ir.DataType.DOUBLE),
            ir.SequenceType(ir.TensorType(ir.DataType.INT32)),
            ir.SequenceType(ir.TensorType(ir.DataType.INT64)),
            ir.SequenceType(ir.TensorType(ir.DataType.FLOAT)),
            ir.SequenceType(ir.TensorType(ir.DataType.DOUBLE)),
        } and all(isinstance(i, (int)) for i in value):
            # We will just allow any fx node and trust that the overload handles it
            return True
        if param.type_constraint.allowed_types & {
            ir.TensorType(ir.DataType.FLOAT),
            ir.TensorType(ir.DataType.DOUBLE),
            ir.SequenceType(ir.TensorType(ir.DataType.FLOAT)),
            ir.SequenceType(ir.TensorType(ir.DataType.DOUBLE)),
        } and all(isinstance(i, (int, float)) for i in value):
            # We will just allow any fx node and trust that the overload handles it
            return True
    if value is None and not param.required:
        # An optional parameter is not supplied
        return True

    if not isinstance(value, ir.TypeProtocol):
        return False

    # Then check tensor types
    if param.type_constraint.name in assigned_types:
        # If a typevar is already bound, check if the value has the same type
        assigned_type = assigned_types[param.type_constraint.name]
        return assigned_type == value
    # If the typevar is not bound, bind it to the value type
    if value in param.type_constraint.allowed_types:
        # TODO: Maybe just check dtype? Being more strict here for now
        assigned_types[param.type_constraint.name] = value
        return True
    return False
