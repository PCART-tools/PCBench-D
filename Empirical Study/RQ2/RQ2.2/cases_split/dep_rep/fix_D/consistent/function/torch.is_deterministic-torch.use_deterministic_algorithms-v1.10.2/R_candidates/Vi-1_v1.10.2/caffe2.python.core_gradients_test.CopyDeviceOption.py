def CopyDeviceOption(op, src_op):
    if src_op.HasField('device_option'):
        op.device_option.CopyFrom(src_op.device_option)
    return op
