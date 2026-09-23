def build_raw_tensor_meta(
    shape=None,
    dtype=None,
    requires_grad=None,
    stride=None,
    memory_format=None,
    is_quantized=None,
    qparams=None,
):
    return TensorMetadata(**locals())
