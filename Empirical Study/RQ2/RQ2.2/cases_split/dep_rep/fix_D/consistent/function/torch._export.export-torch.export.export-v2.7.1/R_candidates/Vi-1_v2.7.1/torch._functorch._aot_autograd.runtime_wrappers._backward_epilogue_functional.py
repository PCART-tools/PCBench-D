def _backward_epilogue_functional(
    metadata, maybe_subclass_metadata, out, *, make_subclass_override=None
):
    # Toss out the backward output tokens
    num_bw_tokens = metadata.num_backward_tokens
    if num_bw_tokens > 0:
        out = out[:-num_bw_tokens]

    # TODO: replace this with FunctionalizedRngRuntimeWrapper.post_compile
    out = FunctionalizedRngRuntimeWrapper()._functionalized_rng_runtime_epilogue(
        metadata, out, offset_index=len(out) - 1
    )
    out = tuple(out)

    # TODO: figure out how to refactor the backward properly so I can use aot_dispatch_subclass_wrapper() here.
    if maybe_subclass_metadata is not None:
        assert maybe_subclass_metadata.grad_input_metas is not None
        outs_wrapped = wrap_tensor_subclasses(
            out,
            subclass_metas=maybe_subclass_metadata.grad_input_metas,
            included_subclass_symints=True,
            is_runtime=True,
            make_subclass_override=make_subclass_override,
        )
        return outs_wrapped
    return out
