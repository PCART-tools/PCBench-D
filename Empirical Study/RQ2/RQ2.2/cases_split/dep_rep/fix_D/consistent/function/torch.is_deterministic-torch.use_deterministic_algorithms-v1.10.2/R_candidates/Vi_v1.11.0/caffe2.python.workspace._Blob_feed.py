def _Blob_feed(blob, arg, device_option=None):
    # conservative type check to avoid unnecessary import
    if type(arg).__name__ == 'Tensor' and type(arg).__module__ == 'torch':
        import torch
        if isinstance(arg, torch.Tensor):
            assert device_option is None, \
                "device_option doesn't make sense with PyTorch tensors"
            handle = torch._C._tensor_impl_raw_handle(arg)
            blob._wrap_tensor_impl(handle)
            return True  # _feed() returns True for some reason
    if device_option is not None:
        device_option = StringifyProto(device_option)
    return blob._feed(arg, device_option)
