@register_acc_op_mapping(
    op_and_target=(
        "call_function",
        torch.ops.quantized.embedding_bag_4bit_rowwise_offsets,
    )
)
@register_acc_op
def embedding_bag_4bit_rowwise_offsets(
    *,
    weight,
    indices,
    offsets,
    scale_grad_by_freq,
    mode,
    pruned_weights,
    per_sample_weights,
    compressed_indices_mapping,
    include_last_offset,
):
    return torch.ops.quantized.embedding_bag_4bit_rowwise_offsets(**locals())
