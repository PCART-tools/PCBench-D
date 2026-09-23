def swap_first_concat_relu(net, ignore_op_with_output=None):
    net = copy.deepcopy(net)

    for ((i, current), (j, next_)) in pairwise(enumerate(net.op)):
        if next_.input[0] != current.output[0]:
            continue

        if current.type != "Concat" or next_.type != "Relu":
            continue

        if ignore_op_with_output and current.output[0] in ignore_op_with_output:
            continue

        # else, can swap
        concat = copy.deepcopy(current)
        relu = copy.deepcopy(next_)
        pre_ops = copy.deepcopy(net.op[:i])
        post_ops = copy.deepcopy(net.op[j + 1 :])

        # Delete the Relu after Concat
        concat.output[0] = relu.output[0]

        # Insert Relu after each op that produces inputs to Concat
        for blob in concat.input:
            k = last_producer(pre_ops, blob)
            producer = pre_ops[k]
            assert producer.output[0] == blob
            producer.output[0] = blob + "_pre_relu"

            new_relu = copy.deepcopy(relu)
            new_relu.input[0] = producer.output[0]
            new_relu.output[0] = blob

            pre_ops = pre_ops[: k + 1] + [new_relu] + pre_ops[k + 1 :]

        new_ops = pre_ops + [concat] + post_ops
        del net.op[:]
        net.op.extend(new_ops)
        break
    return net
