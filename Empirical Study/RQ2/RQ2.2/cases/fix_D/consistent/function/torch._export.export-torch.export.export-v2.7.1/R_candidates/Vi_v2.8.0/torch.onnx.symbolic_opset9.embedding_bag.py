@_onnx_symbolic("aten::embedding_bag")
@symbolic_helper.quantized_args(True)
@symbolic_helper.parse_args("v", "v", "v", "i", "i", "i", "v", "i", "i")
def embedding_bag(
    g: jit_utils.GraphContext,
    embedding_matrix,
    indices,
    offsets,
    scale_grad_by_freq,
    mode,
    sparse,
    per_sample_weights,
    include_last_offset,
    padding_idx,
):
    if not symbolic_helper._is_none(per_sample_weights):
        return symbolic_helper._onnx_unsupported(
            "embedding_bag with per_sample_weights"
        )

    return symbolic_helper._onnx_unsupported("embedding_bag", embedding_matrix)
