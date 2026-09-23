def _rebuild_device_tensor_from_numpy(data, dtype, device, requires_grad):
    tensor = torch.from_numpy(data).to(dtype=dtype, device=device)
    tensor.requires_grad = requires_grad
    return tensor
