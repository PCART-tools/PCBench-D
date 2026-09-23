@tensorrt_converter(acc_ops.flatten)
def acc_ops_flatten(network, target, args, kwargs, name):
    input_val = kwargs["input"]

    if not isinstance(input_val, trt.tensorrt.ITensor):
        raise RuntimeError(
            f"flatten received input {input_val} that is not part "
            "of the TensorRT region!"
        )

    num_dims = len(input_val.shape) + (1 if network.has_implicit_batch_dimension else 0)
    start_dim = (kwargs["start_dim"] if "start_dim" in kwargs else 0) % num_dims
    end_dim = (kwargs["end_dim"] if "end_dim" in kwargs else -1) % num_dims

    if network.has_implicit_batch_dimension:
        assert start_dim != 0, "Can't flatten batch dimension when it's implicit."
        start_dim -= 1
        end_dim -= 1

    layer = network.add_shuffle(input_val)
    layer.name = name

    # If there're dynamic shapes then we need to use shape layers
    # to figure out the final shape after flatten. We first slice
    # the input shape to three parts:
    #   1. dimensions before start_dim
    #   2. dimensions between start_dim and end_dim
    #   3. dimensions after end_dim
    # Part 1 and 3 might not exist if start_dim is 0 or end_dim is
    # last dim. Then we do a reduced multiplication over part 2 to
    # get flattened dim. Finally, we concatenate the three parts to
    # get the final shape.
    if has_dynamic_shape(input_val.shape):
        input_shape_layer = network.add_shape(input_val)
        input_shape_layer.name = f"{name}_orig_shape"

        final_shapes = []

        # Shapes before start_dim
        if start_dim > 0:
            prefix_shape_layer = network.add_slice(
                input_shape_layer.get_output(0),
                start=(0,),
                shape=(start_dim,),
                stride=(1,),
            )
            prefix_shape_layer.name = f"{name}_pre_shape"
            final_shapes.append(prefix_shape_layer.get_output(0))

        flatten_shape_layer = network.add_slice(
            input_shape_layer.get_output(0),
            start=(start_dim,),
            shape=(end_dim - start_dim + 1,),
            stride=(1,),
        )
        flatten_shape_layer.name = f"{name}_need_flatten"
        flatten_shape_layer = network.add_reduce(
            flatten_shape_layer.get_output(0),
            trt.ReduceOperation.PROD,
            axes=get_axes_for_reduce_op(0, False),
            keep_dims=True,
        )
        flatten_shape_layer.name = f"{name}_flatten_dim"
        final_shapes.append(flatten_shape_layer.get_output(0))

        # Shapes after start_dim
        if end_dim < len(input_val.shape) - 1:
            suffix_shape_layer = network.add_slice(
                input_shape_layer.get_output(0),
                start=(end_dim + 1,),
                shape=(len(input_val.shape) - end_dim - 1,),
                stride=(1,),
            )
            suffix_shape_layer.name = f"{name}_suffix_shape"
            final_shapes.append(suffix_shape_layer.get_output(0))

        final_shape_layer = network.add_concatenation(final_shapes)
        final_shape_layer.axis = 0
        final_shape_layer.name = f"{name}_final_shape"
        layer.set_input(1, final_shape_layer.get_output(0))
    else:
        final_shape = []
        flatten_dim = 1
        for i, s in enumerate(input_val.shape):
            if i >= start_dim and i <= end_dim:
                flatten_dim *= s
            elif i == end_dim + 1:
                final_shape.append(flatten_dim)
                final_shape.append(s)
            else:
                final_shape.append(s)
        if end_dim == len(input_val.shape) - 1:
            final_shape.append(flatten_dim)

        layer.reshape_dims = tuple(final_shape)

    return layer.get_output(0)
