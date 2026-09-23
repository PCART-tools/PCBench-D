def validate_cuda_device(location):
    device = torch.cuda._utils._get_device_index(location, True)

    if not torch.cuda.is_available():
        raise RuntimeError('Attempting to deserialize object on a CUDA '
                           'device but torch.cuda.is_available() is False. '
                           'If you are running on a CPU-only machine, '
                           'please use torch.load with map_location=torch.device(\'cpu\') '
                           'to map your storages to the CPU.')
    device_count = torch.cuda.device_count()
    if device >= device_count:
        raise RuntimeError('Attempting to deserialize object on CUDA device '
                           f'{device} but torch.cuda.device_count() is {device_count}. Please use '
                           'torch.load with map_location to map your storages '
                           'to an existing device.')
    return device
