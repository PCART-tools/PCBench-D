def fuse_first_mul_add(net, params, removed_tensors):
    net = copy.deepcopy(net)
    params = copy.deepcopy(params)

    for ((i, current), (j, next_)) in pairwise(enumerate(net.op)):
        if current.type != "Mul" or next_.type != "Add":
            continue

        if next_.input[0] != current.output[0]:
            raise Exception("Failure to fuse")

        if len(blob_uses(net, current.output[0])) != 1:
            raise Exception("Failure to fuse")

        log.info("Fusing at index %s", i)
        mul_ = current
        add_ = next_
        batch_norm = copy.deepcopy(mul_)
        batch_norm.type = "SpatialBN"
        batch_norm.arg.extend([utils.MakeArgument("is_test", 1)])
        batch_norm.arg.extend([utils.MakeArgument("epsilon", float(1e-9))])

        def s(x):
            return "{}{}".format(add_.output[0], x)
        fake_mean = s("_mean")
        fake_var = s("_var")

        del batch_norm.input[:]
        batch_norm.input.extend([mul_.input[0],
                                 mul_.input[1],
                                 add_.input[1],
                                 fake_mean,
                                 fake_var])
        params[fake_mean] = np.zeros_like(params[mul_.input[1]])
        params[fake_var] = np.ones_like(params[mul_.input[1]])
        net.external_input.extend([fake_mean, fake_var])

        batch_norm.output[0] = add_.output[0]
        new_ops = net.op[:i] + [batch_norm] + net.op[j + 1:]
        del net.op[:]
        net.op.extend(new_ops)
        break
    return net, params, removed_tensors
