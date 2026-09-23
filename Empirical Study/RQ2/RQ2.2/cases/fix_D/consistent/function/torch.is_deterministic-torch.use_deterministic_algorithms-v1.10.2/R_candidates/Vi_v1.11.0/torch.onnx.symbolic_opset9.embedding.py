@parse_args("v", "v", "i", "b", "v")
def embedding(g, weight, indices, padding_idx, scale_grad_by_freq, sparse):
    if scale_grad_by_freq and sym_help._training_mode:
        raise RuntimeError("Unsupported: ONNX export of embedding with scale_grad_by_freq=True "
                           "for training mode. ONNX does not support scaling the gradients.")
    if padding_idx >= 0 and sym_help._training_mode:
        warnings.warn("Warning: ONNX export of embedding with padding_idx >= 0 "
                      "for training mode. "
                      "ONNX does not support not updating the embedding vector at padding_idx during training.")

    return g.op("Gather", weight, indices)
