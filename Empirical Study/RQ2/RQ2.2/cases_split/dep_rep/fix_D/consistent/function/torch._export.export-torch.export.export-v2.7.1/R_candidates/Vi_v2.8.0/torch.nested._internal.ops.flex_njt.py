@flex_attention_hop.py_impl(NestedTensor)  # type: ignore[misc]
def flex_njt(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    score_mod: Callable,
    block_mask: Tuple,
    scale: float,
    kernel_options: Dict[str, Any],
    score_mod_other_buffers: Tuple = (),
    mask_mod_other_buffers: Tuple = (),
) -> Tuple[torch.Tensor, torch.Tensor]:
    assert query.dim() == 4 and key.dim() == 4 and value.dim() == 4

    # TODO: Support this if needed; determine if NJT buffers need be unwrapped as dense.
    if any(
        isinstance(buf, torch.Tensor) and buf.is_nested
        for buf in score_mod_other_buffers + mask_mod_other_buffers
    ):
        raise RuntimeError(
            "flex_attention(): Nested tensor score_mod / mask_mod buffers are not "
            "currently supported. Please file an issue if this is important to you."
        )

    # need to pass dense tensor of shape (B, n_heads, sum(seq_len), D)
    output = flex_attention_hop(
        query.values().unsqueeze(0),
        key.values().unsqueeze(0),
        value.values().unsqueeze(0),
        score_mod=score_mod,
        block_mask=block_mask,
        scale=scale,
        kernel_options=kernel_options,
        score_mod_other_buffers=score_mod_other_buffers,
        mask_mod_other_buffers=mask_mod_other_buffers,
    )

    # wrap outputs as NJT
    output_njt = torch.nested.nested_tensor_from_jagged(
        output[0].transpose(1, 2).squeeze(0),
        query._offsets,  # type: ignore[attr-defined]
        query._lengths,  # type: ignore[attr-defined]
        min_seqlen=query._maybe_min_seqlen,  # type: ignore[attr-defined]
        max_seqlen=query._maybe_max_seqlen,  # type: ignore[attr-defined]
    ).transpose(1, 2)

    logsumexp_njt = torch.nested.nested_tensor_from_jagged(
        output[1].transpose(1, 2).squeeze(0),
        query._offsets,  # type: ignore[attr-defined]
        query._lengths,  # type: ignore[attr-defined]
        min_seqlen=query._maybe_min_seqlen,  # type: ignore[attr-defined]
        max_seqlen=query._maybe_max_seqlen,  # type: ignore[attr-defined]
    ).transpose(1, 2)

    return (output_njt, logsumexp_njt)
