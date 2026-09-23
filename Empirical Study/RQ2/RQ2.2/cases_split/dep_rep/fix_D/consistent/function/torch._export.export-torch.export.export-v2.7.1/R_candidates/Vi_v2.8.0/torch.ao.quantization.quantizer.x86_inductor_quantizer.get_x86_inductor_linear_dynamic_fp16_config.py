@functools.lru_cache
def get_x86_inductor_linear_dynamic_fp16_config():
    """
    For linear_dynamic_fp16. The name may be confusing.
    The op's behavior is fp32_input * (fp16_weight -> to_fp32) -> fp32_output.
    """
    weight_quantization_spec = QuantizationSpec(
        dtype=torch.float16,
        observer_or_fake_quant_ctr=PlaceholderObserver,
    )
    quantization_config = QuantizationConfig(
        None,  # input_quantization_spec
        None,  # output_quantization_spec
        weight_quantization_spec,
        None,  # bias_quantization_spec
    )
    return quantization_config
