def tree_flatten_spec(pytree: PyTree, spec: TreeSpec) -> List[Any]:
    if isinstance(spec, LeafSpec):
        return [pytree]
    if spec.type not in SUPPORTED_NODES:
        raise RuntimeError(
            f"{type(pytree)} does not have a flatten_fn_spec associated with it. Please register one with"
            "torch.fx._pytree.register_pytree_flatten_spec.  If you have serialized your model, make"
            "sure that any custom pytrees have been registered before loading it.")
    flatten_fn_spec = SUPPORTED_NODES[spec.type]
    child_pytrees = flatten_fn_spec(pytree, spec)
    result = []
    for child, child_spec in zip(child_pytrees, spec.children_specs):
        flat = tree_flatten_spec(child, child_spec)
        result += flat
    return result
