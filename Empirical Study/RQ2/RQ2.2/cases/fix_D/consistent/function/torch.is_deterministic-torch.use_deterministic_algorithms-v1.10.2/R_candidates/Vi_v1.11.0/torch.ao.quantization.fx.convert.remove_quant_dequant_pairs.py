def remove_quant_dequant_pairs(quantized: QuantizedGraphModule) -> QuantizedGraphModule:
    quantized_root = quantized
    for node in quantized.graph.nodes:
        if node.op == "call_function" and node.target in [torch.quantize_per_tensor, torch.quantize_per_channel]:
            users = list(node.users)
            user = users[0] if users else None
            if len(users) == 1 and user.op == "call_method" and user.target == "dequantize":
                user.replace_all_uses_with(node.args[0])
                quantized.graph.erase_node(user)
                orig_args = list(node.args)
                quantized.graph.erase_node(node)
                for arg in orig_args:
                    if isinstance(arg, Node) and len(list(arg.users)) == 0:
                        quantized.graph.erase_node(arg)

    quantized = QuantizedGraphModule(quantized_root, quantized.graph, quantized_root.preserved_attr_names)
    return quantized
