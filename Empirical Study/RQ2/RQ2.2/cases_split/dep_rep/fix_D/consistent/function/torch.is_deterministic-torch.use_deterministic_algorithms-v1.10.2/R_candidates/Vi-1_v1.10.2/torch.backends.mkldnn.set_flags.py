def set_flags(_enabled):
    orig_flags = (torch._C._get_mkldnn_enabled(),)
    torch._C._set_mkldnn_enabled(_enabled)
    return orig_flags
