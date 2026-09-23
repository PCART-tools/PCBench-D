def is_cuda_tensor(obj):
    return isinstance(obj, torch.Tensor) and obj.is_cuda and not isinstance(obj, torch._subclasses.FakeTensor)
