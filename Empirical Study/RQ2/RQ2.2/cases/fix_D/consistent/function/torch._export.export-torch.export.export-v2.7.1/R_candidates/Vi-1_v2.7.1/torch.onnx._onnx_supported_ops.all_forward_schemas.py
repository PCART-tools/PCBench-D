def all_forward_schemas() -> dict[str, _TorchSchema]:
    """Returns schemas for all TorchScript forward ops."""
    torch_schemas = [_TorchSchema(s) for s in _C._jit_get_all_schemas()]
    return {schema.name: schema for schema in torch_schemas if not schema.is_backward()}
