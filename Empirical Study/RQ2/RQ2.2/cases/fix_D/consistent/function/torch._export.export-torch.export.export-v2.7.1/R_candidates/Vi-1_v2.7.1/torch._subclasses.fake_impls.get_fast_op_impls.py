@functools.lru_cache(None)
def get_fast_op_impls():
    import torch._refs

    register_fast_op_impl(torch.ops.aten.add.Tensor)(
        make_fast_binary_impl(torch._refs.add)
    )
    register_fast_op_impl(torch.ops.aten.sub.Tensor)(
        make_fast_binary_impl(torch._refs.sub)
    )
    register_fast_op_impl(torch.ops.aten.mul.Tensor)(make_fast_binary_impl(torch._refs.mul))  # type: ignore[has-type]
    register_fast_op_impl(torch.ops.aten.div.Tensor)(
        make_fast_binary_impl(torch._refs.div)
    )
    register_fast_op_impl(torch.ops.aten.detach.default)(fast_detach)
    return FAST_OP_IMPLEMENTATIONS
