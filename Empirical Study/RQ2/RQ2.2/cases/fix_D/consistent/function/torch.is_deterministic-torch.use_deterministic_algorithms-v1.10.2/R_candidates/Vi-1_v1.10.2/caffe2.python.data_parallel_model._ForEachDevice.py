def _ForEachDevice(devices, f, device_type, device_prefix, scoped=False,
                   *args, **kwargs):
    for device in devices:
        device_opt = core.DeviceOption(device_type, device)
        with core.DeviceScope(device_opt):
            if scoped:
                with core.NameScope("{}_{}".format(device_prefix, device)):
                    f(device, *args, **kwargs)
            else:
                f(device, *args, **kwargs)
