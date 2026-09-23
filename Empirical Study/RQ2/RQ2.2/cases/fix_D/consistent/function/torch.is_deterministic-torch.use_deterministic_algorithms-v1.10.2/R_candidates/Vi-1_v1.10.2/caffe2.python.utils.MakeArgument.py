def MakeArgument(key, value):
    """Makes an argument based on the value type."""
    argument = caffe2_pb2.Argument()
    argument.name = key
    iterable = isinstance(value, collections.abc.Iterable)

    # Fast tracking common use case where a float32 array of tensor parameters
    # needs to be serialized.  The entire array is guaranteed to have the same
    # dtype, so no per-element checking necessary and no need to convert each
    # element separately.
    if isinstance(value, np.ndarray) and value.dtype.type is np.float32:
        argument.floats.extend(value.flatten().tolist())
        return argument

    if isinstance(value, np.ndarray):
        value = value.flatten().tolist()
    elif isinstance(value, np.generic):
        # convert numpy scalar to native python type
        value = np.asscalar(value)

    if type(value) is float:
        argument.f = value
    elif type(value) in integer_types or type(value) is bool:
        # We make a relaxation that a boolean variable will also be stored as
        # int.
        argument.i = value
    elif isinstance(value, binary_type):
        argument.s = value
    elif isinstance(value, text_type):
        argument.s = value.encode('utf-8')
    elif isinstance(value, caffe2_pb2.NetDef):
        argument.n.CopyFrom(value)
    elif isinstance(value, Message):
        argument.s = value.SerializeToString()
    elif iterable and all(type(v) in [float, np.float_] for v in value):
        argument.floats.extend(
            v.item() if type(v) is np.float_ else v for v in value
        )
    elif iterable and all(
        type(v) in integer_types or type(v) in [bool, np.int_] for v in value
    ):
        argument.ints.extend(
            v.item() if type(v) is np.int_ else v for v in value
        )
    elif iterable and all(
        isinstance(v, binary_type) or isinstance(v, text_type) for v in value
    ):
        argument.strings.extend(
            v.encode('utf-8') if isinstance(v, text_type) else v
            for v in value
        )
    elif iterable and all(isinstance(v, caffe2_pb2.NetDef) for v in value):
        argument.nets.extend(value)
    elif iterable and all(isinstance(v, Message) for v in value):
        argument.strings.extend(v.SerializeToString() for v in value)
    else:
        if iterable:
            raise ValueError(
                "Unknown iterable argument type: key={} value={}, value "
                "type={}[{}]".format(
                    key, value, type(value), set(type(v) for v in value)
                )
            )
        else:
            raise ValueError(
                "Unknown argument type: key={} value={}, value type={}".format(
                    key, value, type(value)
                )
            )
    return argument
