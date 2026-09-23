def build_raw_tensor_meta(
    shape=None,
    dtype=None,
    requires_grad=None,
    stride=None,
    memory_format=None,
    is_quantized=None,
    qscheme=None,
    q_scale=None,
    q_zero_point=None,
):
    return TensorMetadata(**locals())
