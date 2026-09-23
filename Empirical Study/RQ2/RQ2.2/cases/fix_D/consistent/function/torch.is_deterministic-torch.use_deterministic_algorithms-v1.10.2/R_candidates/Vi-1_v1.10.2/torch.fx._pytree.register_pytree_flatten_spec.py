def register_pytree_flatten_spec(typ: Any, flatten_fn_spec: FlattenFuncSpec) -> None:
    SUPPORTED_NODES[typ] = flatten_fn_spec
