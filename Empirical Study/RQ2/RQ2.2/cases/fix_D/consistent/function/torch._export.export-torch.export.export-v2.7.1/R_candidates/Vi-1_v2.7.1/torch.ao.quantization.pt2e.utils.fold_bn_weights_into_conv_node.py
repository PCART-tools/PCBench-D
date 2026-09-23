def fold_bn_weights_into_conv_node(
    conv_node: Node,
    conv_weight_node: Node,
    conv_bias_node: Optional[Node],
    bn_node: Node,
    m: GraphModule,
) -> None:
    # conv args: input, weight, bias, stride, padding, dilation, ...
    conv_w = _get_tensor_constant_from_node(conv_weight_node, m)
    conv_b = _get_tensor_constant_from_node(conv_bias_node, m)
    transpose = _is_conv_transpose_node(conv_node)

    # eval bn args: input, weight, bias, running mean, running var, momentum, eps
    # train bn args: input, weight, bias, running mean, running var, training, momentum, eps
    bn_args_schema = bn_node.target._schema.arguments  # type: ignore[union-attr]
    bn_args = _get_all_arguments(bn_node.args, bn_node.kwargs, bn_args_schema)
    bn_w = _get_tensor_constant_from_node(bn_args[1], m)
    bn_b = _get_tensor_constant_from_node(bn_args[2], m)
    bn_rm = _get_tensor_constant_from_node(bn_args[3], m)
    bn_rv = _get_tensor_constant_from_node(bn_args[4], m)
    if bn_node.target == torch.ops.aten._native_batch_norm_legit_no_training.default:
        eps_arg_index = 6
    elif _is_supported_batch_norm_for_training(bn_node):
        eps_arg_index = 7
    else:
        raise ValueError("BN node target is unexpected ", bn_node.target)
    bn_eps = bn_args[eps_arg_index]

    fused_weight, fused_bias = fuse_conv_bn_weights(
        conv_w, conv_b, bn_rm, bn_rv, bn_eps, bn_w, bn_b, transpose=transpose
    )

    # update the weight and bias for conv
    conv_args = list(conv_node.args)
    # filling in the default bias argument
    if len(conv_args) == 2:
        conv_args.append(None)

    # calling data since the fused_weight and fused_bias are nn.Parameter
    weight_attr_name = conv_weight_node.target
    assert isinstance(weight_attr_name, str)
    _assign_attr(fused_weight, m, weight_attr_name, _AttrKind.PARAMETER)
    if conv_bias_node is not None:
        bias_attr_name = conv_bias_node.target
        _assign_attr(fused_bias, m, str(bias_attr_name), _AttrKind.PARAMETER)
    else:
        bias_attr_name = weight_attr_name + "_bias"
        _assign_attr(fused_bias, m, bias_attr_name, _AttrKind.PARAMETER)
        with m.graph.inserting_before(conv_node):
            get_bias_node = m.graph.get_attr(bias_attr_name)
        # NOTE: here we assume the bias of conv is not quantized!
        conv_args[2] = get_bias_node
    conv_node.args = tuple(conv_args)

    # native_batch_norm has 3 outputs, we expect getitem calls on the output
    # and we want to replace the uses of getitem 0 with the output of conv
    #
    if bn_node.target == torch.ops.aten.batch_norm.default:
        # With the new training ir, instead of batch_norm + getitem,
        # we only have the batch_norm node.
        #
        # Before:
        # conv -> bn -> users
        # After:
        # conv -> users
        #       bn has no users now
        bn_node.replace_all_uses_with(conv_node)
    else:
        # Before:
        # conv -> bn - (first output) -> users1
        #          \ - (second output) -> users2
        #          \ - (third output) -> users3
        # After:
        # conv -> (first output) -> users1
        #       bn -
        #          \ - (second output) -> users2
        #          \ - (third output) -> users3
        # if users2 and users3 are empty then bn will be removed through dead code elimination
        for user in bn_node.users:
            if (
                user.op != "call_function"
                or user.target != operator.getitem
                or user.args[1] != 0
            ):
                continue
            user.replace_all_uses_with(conv_node)

    # If the BN node does not have users, erase it from the graph
    # Note: we need to do this manually because the model can still be in train
    # mode at this point, in which case DCE won't erase the BN node automatically
    # since the node refers to a mutating op. Here we still need to call DCE first
    # to get rid of the unused getitem nodes that consume the BN node.
    m.graph.eliminate_dead_code()
    if len(bn_node.users) == 0:
        m.graph.erase_node(bn_node)
