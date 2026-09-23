def _register_pytree_node(typ: Any, flatten_fn: FlattenFunc, unflatten_fn: UnflattenFunc) -> None:
    SUPPORTED_NODES[typ] = NodeDef(flatten_fn, unflatten_fn)
