def _cuda_deserialize(obj, location):
    if location.startswith('cuda'):
        device = validate_cuda_device(location)
        if getattr(obj, "_torch_load_uninitialized", False):
            storage_type = getattr(torch.cuda, type(obj).__name__)
            with torch.cuda.device(device):
                return storage_type(obj.size())
        else:
            return obj.cuda(device)
