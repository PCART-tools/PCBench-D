def BoolNet(*blobs_with_bool_value):
    """A net assigning constant bool values to blobs. It is mainly used for
    initializing condition blobs, for example, in multi-task learning, we
    need to access reader_done blobs before reader_net run. In that case,
    the reader_done blobs must be initialized.

    Args:
    blobs_with_bool_value: one or more (blob, bool_value) pairs. The net will
    assign each bool_value to the corresponding blob.

    returns
    bool_net: A net assigning constant bool values to blobs.

    Examples:
    - BoolNet((blob_1, bool_value_1), ..., (blob_n, bool_value_n))
    - BoolNet([(blob_1, net1), ..., (blob_n, bool_value_n)])
    - BoolNet((cond_1, bool_value_1))
    """
    blobs_with_bool_value = _MakeList(blobs_with_bool_value)
    bool_net = core.Net('bool_net')
    for blob, bool_value in blobs_with_bool_value:
        out_blob = bool_net.ConstantFill(
            [],
            [blob],
            shape=[],
            value=bool_value,
            dtype=core.DataType.BOOL)
        bool_net.AddExternalOutput(out_blob)

    return bool_net
