def format_device_option(dev_opt):
    if not dev_opt or not (
            dev_opt.device_type or dev_opt.device_id or dev_opt.node_name):
        return None
    return call(
        'DeviceOption',
        [dev_opt.device_type, dev_opt.device_id, "'%s'" % dev_opt.node_name])
