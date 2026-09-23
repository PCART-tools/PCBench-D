def set_flags(_enabled):
    r"""Set if nnpack is enabled globally"""
    orig_flags = (torch._C._get_nnpack_enabled(),)
    torch._C._set_nnpack_enabled(_enabled)
    return orig_flags
