def InjectDeviceCopiesAmongNetsWithoutB2D(nets, blob_to_device_init=None):
    new_nets, _ = InjectDeviceCopiesAmongNets(nets, blob_to_device_init)
    return new_nets
