def _sdpa_backward_handler(
    op_call: torch._ops.OpOverload,
    args: tuple[object, ...],
    kwargs: dict[str, object],
) -> object:
    # Redistribute grad_output tensor to the same placement as output tensor
    args = list(args)
    args = tuple(args)

    # extract local tensor and sharding infos to a OpInfo
    op_info = DTensor._op_dispatcher.unwrap_to_op_info(op_call, args, kwargs)
    logger.debug("Dispatching op_call: %s", op_info.schema)

    # sharding propagation
    DTensor._op_dispatcher.sharding_propagator.propagate(op_info)
    output_sharding = op_info.output_sharding
    assert output_sharding is not None, "output sharding should not be None"
    assert not output_sharding.needs_redistribute, "inputs need to be redistributed"

    if op_call == aten._scaled_dot_product_flash_attention_backward.default:
        local_results = _scaled_dot_product_ring_flash_attention_backward(
            op_info.compute_mesh,
            *op_info.local_args,  # type: ignore[arg-type]
            **op_info.local_kwargs,  # type: ignore[arg-type]
        )
    elif op_call == aten._scaled_dot_product_efficient_attention_backward.default:
        local_results = _scaled_dot_product_ring_efficient_attention_backward(
            op_info.compute_mesh,
            *op_info.local_args,  # type: ignore[arg-type]
            **op_info.local_kwargs,  # type: ignore[arg-type]
        )
    elif op_call == aten._scaled_dot_product_cudnn_attention_backward.default:
        local_results = _scaled_dot_product_ring_cudnn_attention_backward(
            op_info.compute_mesh,
            *op_info.local_args,  # type: ignore[arg-type]
            **op_info.local_kwargs,  # type: ignore[arg-type]
        )
    else:
        raise NotImplementedError(f"{op_call=}")

    return DTensor._op_dispatcher.wrap(local_results, output_sharding.output_spec)
