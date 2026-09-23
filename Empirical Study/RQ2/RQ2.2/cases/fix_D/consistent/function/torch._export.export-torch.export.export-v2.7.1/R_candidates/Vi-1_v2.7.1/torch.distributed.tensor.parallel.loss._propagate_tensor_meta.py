def _propagate_tensor_meta(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> TensorMeta:
    op_info = DTensor._op_dispatcher.unwrap_to_op_info(op_call, args, kwargs)
    tensor_meta = DTensor._op_dispatcher.sharding_propagator._propagate_tensor_meta(
        op_info.schema
    )
    if isinstance(tensor_meta, TensorMeta):
        return tensor_meta
    elif isinstance(tensor_meta, tuple):
        return tensor_meta[0]
    else:
        raise RuntimeError(f"Unexpected tensor meta type: {type(tensor_meta)}.")
