def _mark_nodes_as_annotated(nodes: list[Node]):
    for node in nodes:
        if node is not None:
            if QUANT_ANNOTATION_KEY not in node.meta:
                node.meta[QUANT_ANNOTATION_KEY] = _X86InductorQuantizationAnnotation()
            node.meta[QUANT_ANNOTATION_KEY]._annotated = True
