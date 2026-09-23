def remove_extra_dequantize(quantized: QuantizedGraphModule) -> QuantizedGraphModule:
    """
    Removes duplicate dequant nodes in the graph, for an operator that has multiple dequant nodes as a user,
    replace them with a single dequant node that can be shared across all the uses.
    """
    quantized_root = quantized
    for node in quantized.graph.nodes:
        users = list(node.users)
        dequant_users = [user for user in node.users if user.op == "call_method" and user.target == "dequantize" or
                         (user.op == "call_function" and user.target == torch.dequantize)]

        if len(dequant_users) > 1:
            with quantized.graph.inserting_after(node):
                unique_dq = quantized.graph.create_node("call_method", "dequantize", users[0].args, {})
            for dequant in dequant_users:
                dequant.replace_all_uses_with(unique_dq)
                quantized.graph.erase_node(dequant)

    quantized = QuantizedGraphModule(quantized_root, quantized.graph, quantized_root.preserved_attr_names)
    return quantized
