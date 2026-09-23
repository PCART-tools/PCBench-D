def is_tensor_getset_descriptor(name):
    try:
        attr = inspect.getattr_static(torch.Tensor, name)
        return type(attr) is types.GetSetDescriptorType
    except AttributeError:
        return False
