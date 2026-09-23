def _convert_to_mil_type(spec: _TensorSpec, name: str):
    ml_type = TensorType(shape=spec.shape, dtype=torch_to_mil_types[spec.dtype])
    ml_type.name = name
    return ml_type
