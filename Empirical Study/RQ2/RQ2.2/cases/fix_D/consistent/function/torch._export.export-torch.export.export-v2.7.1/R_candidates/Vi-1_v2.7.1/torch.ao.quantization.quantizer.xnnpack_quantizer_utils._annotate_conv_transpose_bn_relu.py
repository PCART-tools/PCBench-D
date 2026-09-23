@register_annotator("conv_transpose_bn_relu")
def _annotate_conv_transpose_bn_relu(
    gm: torch.fx.GraphModule,
    quantization_config: Optional[QuantizationConfig],
    filter_fn: Optional[Callable[[Node], bool]] = None,
) -> Optional[list[list[Node]]]:
    """
    Find conv_transpose + batchnorm + relu parititions
    Note: This is only used for QAT. In PTQ, batchnorm should already be fused into the conv.
    """
    return _do_annotate_conv_bn(
        gm, quantization_config, filter_fn, has_relu=True, is_conv_transpose=True
    )
