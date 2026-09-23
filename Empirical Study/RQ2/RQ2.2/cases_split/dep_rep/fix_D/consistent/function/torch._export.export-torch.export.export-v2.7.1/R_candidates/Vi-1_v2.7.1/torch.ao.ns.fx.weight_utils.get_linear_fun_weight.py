def get_linear_fun_weight(node: Node, gm: GraphModule) -> torch.Tensor:
    # traverse backwards from the weight arg, accounting for any observers
    # supported patterns:
    # weight -> obs -> linear
    # weight -> to(torch.float16) -> dequantize -> linear
    linear_second_arg = node.args[1]
    assert isinstance(linear_second_arg, Node)

    if linear_second_arg.op == "call_module":
        # weight -> obs -> linear
        weight_arg_node = node.args[1]
        assert isinstance(weight_arg_node, Node)
        weight_node = weight_arg_node.args[0]
        assert isinstance(weight_node, Node)
        assert weight_node.op == "get_attr"
        weight = getattr_from_fqn(gm, weight_node.target)  # type: ignore[arg-type]
        return weight.detach()
    elif linear_second_arg.op == "call_method":
        # weight -> to(torch.float16) -> dequantize -> linear
        assert linear_second_arg.op == "call_method"
        dequant_node = node.args[1]
        assert isinstance(dequant_node, Node)
        to_fp16_node = dequant_node.args[0]
        assert isinstance(to_fp16_node, Node)
        # extract the dtype, so we can cast to it before returning
        target_dtype = to_fp16_node.args[1]
        weight_node = to_fp16_node.args[0]
        assert isinstance(weight_node, Node)
        assert weight_node.op == "get_attr"
        weight = getattr_from_fqn(gm, weight_node.target)  # type: ignore[arg-type]
        # return the weight with fp16 cast
        return weight.detach().to(target_dtype)
    else:
        assert linear_second_arg.op == "get_attr"
        weight = getattr_from_fqn(gm, linear_second_arg.target)  # type: ignore[arg-type]
        return weight.detach()
