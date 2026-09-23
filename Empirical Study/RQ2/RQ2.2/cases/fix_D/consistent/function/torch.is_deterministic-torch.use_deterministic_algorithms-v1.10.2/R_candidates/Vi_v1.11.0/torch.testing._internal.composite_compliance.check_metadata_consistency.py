def check_metadata_consistency(wrapper_tensor):
    if not isinstance(wrapper_tensor, CompositeCompliantTensor):
        return
    things_to_check = {
        'shape': Tensor.size,
        'dtype': lambda x: x.dtype,
        'device': lambda x: x.device,
        'numel': Tensor.numel,
        'stride': Tensor.stride,
        'storage_offset': Tensor.storage_offset,
    }
    for metadata_name, metadata_accessor in things_to_check.items():
        check_attr_consistency(wrapper_tensor, metadata_name, metadata_accessor)
