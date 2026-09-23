@register_acc_op_mapping(op_and_target=("call_function", nn.functional.embedding_bag))
@register_acc_op
def embedding_bag(
    *,
    input,
    weight,
    offsets,
    max_norm,
    norm_type,
    scale_grad_by_freq,
    mode,
    sparse,
    per_sample_weights,
    include_last_offset,
    padding_idx,
):
    return nn.functional.embedding_bag(
        input=input,
        weight=weight,
        offsets=offsets,
        max_norm=max_norm,
        norm_type=norm_type,
        scale_grad_by_freq=scale_grad_by_freq,
        mode=mode,
        sparse=sparse,
        per_sample_weights=per_sample_weights,
        include_last_offset=include_last_offset,
        padding_idx=padding_idx,
    )
