def _propagate_device_option(net):
    if not net.HasField("device_option"):
        return
    for op in net.op:
        if not op.HasField("device_option"):
            op.device_option.CopyFrom(net.device_option)
