def dlrm_wrap(X, lS_o, lS_i, device, ndevices=1):
    """Rewritten simpler version of ```dlrm_wrap()``` found in dlrm_s_pytorch.py.
    This function simply moves the input tensors into the device and without the forward pass
    """
    if ndevices == 1:
        lS_i = (
            [S_i.to(device) for S_i in lS_i]
            if isinstance(lS_i, list)
            else lS_i.to(device)
        )
        lS_o = (
            [S_o.to(device) for S_o in lS_o]
            if isinstance(lS_o, list)
            else lS_o.to(device)
        )
    return X.to(device), lS_o, lS_i
