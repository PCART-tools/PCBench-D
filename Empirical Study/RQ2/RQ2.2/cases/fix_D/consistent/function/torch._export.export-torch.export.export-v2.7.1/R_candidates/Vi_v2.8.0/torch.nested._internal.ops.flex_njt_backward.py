@flex_attention_backward_hop.py_impl(NestedTensor)  # type: ignore[misc]
def flex_njt_backward(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    out: torch.Tensor,
    logsumexp: torch.Tensor,
    grad_out: torch.Tensor,
    grad_logsumexp: torch.Tensor,
    fw_graph: Union[Callable, GraphModule],
    joint_graph: GraphModule,
    block_mask: Tuple,
    scale: float,
    kernel_options: Dict[str, Any],
    score_mod_other_buffers: Tuple = (),
    mask_mod_other_buffers: Tuple = (),
) -> Tuple[
    torch.Tensor, torch.Tensor, torch.Tensor, Tuple[Optional[torch.Tensor], ...]
]:
    output = flex_attention_backward_hop(
        query.values().unsqueeze(0),
        key.values().unsqueeze(0),
        value.values().unsqueeze(0),
        out=out.values().unsqueeze(0),
        logsumexp=logsumexp.values().unsqueeze(0),
        grad_out=grad_out.values().unsqueeze(0),
        grad_logsumexp=grad_logsumexp.values().unsqueeze(0),
        fw_graph=fw_graph,
        joint_graph=joint_graph,
        block_mask=block_mask,
        scale=scale,
        kernel_options=kernel_options,
        score_mod_other_buffers=score_mod_other_buffers,
        mask_mod_other_buffers=mask_mod_other_buffers,
    )

    # wrap grads as NJTs
    dense_q_grad, dense_k_grad, dense_v_grad, score_mod_other_buffer_grads = output
    njt_q_grad = torch.nested.nested_tensor_from_jagged(
        dense_q_grad.transpose(1, 2).squeeze(0),
        query._offsets,  # type: ignore[attr-defined]
        query._lengths,  # type: ignore[attr-defined]
        min_seqlen=query._maybe_min_seqlen,  # type: ignore[attr-defined]
        max_seqlen=query._maybe_max_seqlen,  # type: ignore[attr-defined]
    ).transpose(1, 2)
    njt_k_grad = torch.nested.nested_tensor_from_jagged(
        dense_k_grad.transpose(1, 2).squeeze(0),
        key._offsets,  # type: ignore[attr-defined]
        key._lengths,  # type: ignore[attr-defined]
        min_seqlen=key._maybe_min_seqlen,  # type: ignore[attr-defined]
        max_seqlen=key._maybe_max_seqlen,  # type: ignore[attr-defined]
    ).transpose(1, 2)
    njt_v_grad = torch.nested.nested_tensor_from_jagged(
        dense_v_grad.transpose(1, 2).squeeze(0),
        value._offsets,  # type: ignore[attr-defined]
        value._lengths,  # type: ignore[attr-defined]
        min_seqlen=value._maybe_min_seqlen,  # type: ignore[attr-defined]
        max_seqlen=value._maybe_max_seqlen,  # type: ignore[attr-defined]
    ).transpose(1, 2)

    return (njt_q_grad, njt_k_grad, njt_v_grad, score_mod_other_buffer_grads)
