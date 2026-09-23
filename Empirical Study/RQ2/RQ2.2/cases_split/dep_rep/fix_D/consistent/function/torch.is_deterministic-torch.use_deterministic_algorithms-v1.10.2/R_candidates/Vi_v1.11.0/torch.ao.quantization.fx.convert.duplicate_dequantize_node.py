def duplicate_dequantize_node(quantized: QuantizedGraphModule) -> QuantizedGraphModule:
    """
    If a dequantize node has multiple uses, duplicate it and create one dequantize node for each use.
    This is to enable the pattern matching to map from individual quant - dequant - ref_module to
    final quantized module.
    """
    quantized_root = quantized
    for node in quantized.graph.nodes:
        if (node.op == "call_method" and node.target == "dequantize" or
           (node.op == "call_function" and node.target == torch.dequantize)):
            users = list(node.users)
            if len(users) > 1:
                for user in users:
                    with quantized.graph.inserting_before(node):
                        new_node = quantized.graph.create_node("call_method", "dequantize", node.args, {})
                    user.replace_input_with(node, new_node)
                quantized.graph.erase_node(node)

    quantized = QuantizedGraphModule(quantized_root, quantized.graph, quantized_root.preserved_attr_names)
    return quantized
