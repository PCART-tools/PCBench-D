def InjectDeviceCopiesAmongNets(nets, blob_to_device_init=None):
    """
    Takes in a list of nets. They usually represent your whole execution graph.
    This function will insert cross device copy functions to all nets, and resolve
    inter-net external inputs dependencies. This method will insert Copy funcitons if
    external inputs of a net is produced on different device than it is required.
    Inputs:
      nets: a list of nets
    Outputs:
      new_nets: a list of new nets with device difference solved.

    Some notes from wyiming:
      1. You MUST pass nets in execution order. e.g. [train_init, train]
    """
    assert isinstance(nets, list), \
        "nets {} should be a list of nets.".format(str(nets))
    assert all(isinstance(net, Net) for net in nets), \
        "nets {} should be a list of nets.".format(str(nets))
    # A holistic blob to device mapping.
    blob_to_device = blob_to_device_init or {}
    blob_remap = {}
    new_nets = []

    for net in nets:
        new_net, blob_to_device = InjectCrossDeviceCopies(
            net,
            blob_to_device=blob_to_device,
            blob_remap=blob_remap,
        )
        new_nets.append(new_net)

    return new_nets, blob_to_device
