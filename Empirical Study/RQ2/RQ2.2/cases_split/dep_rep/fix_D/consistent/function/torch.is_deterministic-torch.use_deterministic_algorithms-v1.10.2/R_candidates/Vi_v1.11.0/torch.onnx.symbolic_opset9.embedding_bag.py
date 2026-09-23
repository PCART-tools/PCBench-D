@parse_args("v", "v", "v", "i", "i", "i", "v", "i", "i")
def embedding_bag(g,
                  embedding_matrix,
                  indices,
                  offsets,
                  scale_grad_by_freq,
                  mode,
                  sparse,
                  per_sample_weights,
                  include_last_offset,
                  padding_idx):
    if not sym_help._is_none(per_sample_weights):
        return sym_help._onnx_unsupported("embedding_bag  with per_sample_weights")
    if sym_help._operator_export_type == torch.onnx.OperatorExportTypes.ONNX_ATEN_FALLBACK:
        return g.op("ATen",
                    embedding_matrix,
                    indices,
                    offsets,
                    operator_s="embedding_bag",
                    outputs=4,
                    scale_grad_by_freq_i=scale_grad_by_freq,
                    mode_i=mode,
                    sparse_i=sparse,
                    include_last_offset_i=include_last_offset,
                    padding_idx_i=padding_idx)
    else:
        return sym_help._onnx_unsupported("embedding_bag")
