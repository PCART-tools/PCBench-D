def wrap(arg, CCT, cct_mode):
    # CCT: CompositeCompliantTensor class which is generated using generate_cct_and_mode
    if isinstance(arg, torch.Tensor):
        return CCT(arg, cct_mode)
    if is_tensorlist(arg):
        return [CCT(a, cct_mode) for a in arg]
    raise RuntimeError("wrap assumes that the input can be wrapped")
