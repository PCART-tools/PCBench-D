@register_annotator("conv_transpose_relu")
def _annotate_conv_transpose_relu(
    gm: torch.fx.GraphModule,
    quantization_config: Optional[QuantizationConfig],
    filter_fn: Optional[Callable[[Node], bool]] = None,
) -> Optional[list[list[Node]]]:
    return _do_annotate_conv_relu(
        gm, quantization_config, filter_fn, is_conv_transpose=True
    )
