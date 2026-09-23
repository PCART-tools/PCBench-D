def _annotate_output_qspec(node: Node, qspec):
    quantization_annotation = node.meta.get(
        "quantization_annotation", QuantizationAnnotation()
    )
    quantization_annotation.output_qspec = qspec
    node.meta["quantization_annotation"] = quantization_annotation
