def _generate_masked_op_mask(input_shape, device, **kwargs):
    yield None
    yield make_tensor(input_shape, device, torch.bool, requires_grad=False)
    if len(input_shape) > 2:
        # broadcast last mask dimension:
        yield make_tensor(input_shape[:-1] + (1,), device, torch.bool, requires_grad=False)
        # broadcast middle mask dimension:
        yield make_tensor(input_shape[:1] + (1,) + input_shape[2:], device, torch.bool, requires_grad=False)
        # broadcast first mask dimension:
        yield make_tensor((1,) + input_shape[1:], device, torch.bool, requires_grad=False)
        # mask.ndim < input.ndim
        yield make_tensor(input_shape[1:], device, torch.bool, requires_grad=False)
        # mask.ndim == 1
        yield make_tensor(input_shape[-1:], device, torch.bool, requires_grad=False)
