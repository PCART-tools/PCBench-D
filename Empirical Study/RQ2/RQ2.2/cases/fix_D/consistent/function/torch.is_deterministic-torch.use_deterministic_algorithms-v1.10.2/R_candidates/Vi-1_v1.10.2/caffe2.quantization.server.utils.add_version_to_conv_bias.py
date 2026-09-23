def add_version_to_conv_bias(net, init_net):
    """
    In architectures such as FPN (https://arxiv.org/abs/1612.03144), few Conv
    ops share the same weight and bias and are run at different scales of
    the input. Since 'bias_scale = input_scale * weight_scale', sharing the
    same bias blob among multiple Conv ops means that we need different bias
    scale for each of the ops. To achieve this, we just duplicate those bias
    blobs that are used by multiple Conv ops before performing int8 rewrite.
    """
    bias_count = defaultdict(int)
    for op in net._net.op:
        if "Conv" in op.type and len(op.input) >= 3:
            bias_count[op.input[2]] += 1

    bias_fill_op = {}
    for op in init_net._net.op:
        if bias_count[op.output[0]] > 1:
            bias_fill_op[op.output[0]] = op

    bias_version = defaultdict(int)
    for op in net._net.op:
        if "Conv" in op.type and len(op.input) >= 3:
            bias = op.input[2]
            if bias_count[bias] <= 1:
                continue

            version = bias_version[bias]
            bias_version[bias] += 1
            if version == 0:
                continue

            new_bias = bias + "_v" + str(version)
            fill_op = copy.deepcopy(bias_fill_op[bias])
            fill_op.output[0] = new_bias
            init_net._net.op.extend([fill_op])
            op.input[2] = new_bias
            net._net.external_input.append(new_bias)
