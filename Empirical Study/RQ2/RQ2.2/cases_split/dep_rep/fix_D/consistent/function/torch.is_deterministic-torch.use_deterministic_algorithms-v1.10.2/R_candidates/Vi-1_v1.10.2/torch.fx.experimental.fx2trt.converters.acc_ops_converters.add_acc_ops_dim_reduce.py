def add_acc_ops_dim_reduce(network, target, args, kwargs, name, reduce_op):
    new_kwargs = kwargs.copy()
    new_kwargs['k'] = 1


    if reduce_op == trt.ReduceOperation.MAX:
        new_kwargs['largest'] = True
    elif reduce_op == trt.ReduceOperation.MIN:
        new_kwargs['largest'] = False
    new_kwargs['sorted'] = False


    (topk_out0, topk_out1) = acc_ops_topk(network, target, args, new_kwargs, name + "_topk")

    topk_out0.name = f"{name}_topk0"
    topk_out1.name = f"{name}_topk1"

    if 'keepdim' in new_kwargs and new_kwargs['keepdim']:
        return (topk_out0, topk_out1)

    dim = new_kwargs['dim']
    if network.has_implicit_batch_dimension:
        assert dim != 0, "can't reduce on dim == 0 when network has implicit batch dimension"
        # we remove the first dim in the shape tuple when it is implicit
        dim -= 1
    input_val = topk_out0
    shape = input_val.shape

    output_shape = []
    for i, s in enumerate(shape):
        if i == dim and s == 1:
            continue
        output_shape.append(s)

    shuffle_layer0 = network.add_shuffle(input_val)
    shuffle_layer0.reshape_dims = tuple(output_shape)
    shuffle_layer0.name = name + '_shuffle0'

    input_val = topk_out1
    shape = input_val.shape

    shuffle_layer1 = network.add_shuffle(input_val)
    shuffle_layer1.reshape_dims = tuple(output_shape)
    shuffle_layer1.name = name + '_shuffle1'


    return (shuffle_layer0.get_output(0), shuffle_layer1.get_output(0))
