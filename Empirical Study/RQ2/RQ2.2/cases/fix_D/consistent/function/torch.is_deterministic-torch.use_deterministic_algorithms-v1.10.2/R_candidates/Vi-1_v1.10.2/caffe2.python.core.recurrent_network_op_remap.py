def recurrent_network_op_remap(op, prefix, blob_remap):
    """
    Parameters
    ----------
    op : Caffe2 operator (RecurrentNetworkOp or RecurrentNetworkGradientOp).
    prefix: this argument is not used in this function, just for legacy support.
    blob_remap : Dictionary that represents the map from old blob name to new.

    Updates blob names in arguments of RecurrentNetworkOp and
    RecurrentNetworkGradientOp to conform to cloned input and output of both
    operators and also makes sure names of locally generated blobs in arguments
    have the same prefix as the input and output of the operators.
    """

    def get_remapped_str(blob_str):
        if isinstance(blob_str, binary_type):
            blob_str = blob_str.decode('utf-8')
        return blob_remap.get(blob_str, blob_str).encode('utf-8')

    for argument in op.arg:
        if len(argument.strings) > 0:
            for i in range(len(argument.strings)):
                argument.strings[i] = get_remapped_str(argument.strings[i])
        elif argument.name == 'timestep':
            argument.s = get_remapped_str(argument.s)
        elif argument.name.endswith('step_net'):
            # argument is a proto
            remap_proto(argument, blob_remap)
