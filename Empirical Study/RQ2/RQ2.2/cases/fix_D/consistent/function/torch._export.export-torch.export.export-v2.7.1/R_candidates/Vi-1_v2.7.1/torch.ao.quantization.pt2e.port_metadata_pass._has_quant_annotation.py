def _has_quant_annotation(node: torch.fx.Node) -> bool:
    return "quantization_annotation" in node.meta
