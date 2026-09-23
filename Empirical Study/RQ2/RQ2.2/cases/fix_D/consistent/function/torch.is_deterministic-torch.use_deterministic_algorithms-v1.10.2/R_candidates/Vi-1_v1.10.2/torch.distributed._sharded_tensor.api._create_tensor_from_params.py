def _create_tensor_from_params(*size, local_device, tensor_init_params: TensorInitParams):
    """ Helper to construct tensor from size, device and common params. """

    create_op = tensor_init_params.create_op
    dtype = tensor_init_params.tensor_properties.dtype
    layout = tensor_init_params.tensor_properties.layout
    requires_grad = tensor_init_params.tensor_properties.requires_grad
    memory_format = tensor_init_params.tensor_properties.memory_format
    pin_memory = tensor_init_params.tensor_properties.pin_memory

    if create_op == CreateOp.ONES:
        return torch.ones(*size, dtype=dtype, layout=layout,
                          device=local_device, pin_memory=pin_memory,
                          requires_grad=requires_grad,)
    elif create_op == CreateOp.EMPTY:
        return torch.empty(*size, dtype=dtype, layout=layout,
                           device=local_device, requires_grad=requires_grad,
                           # NB: memory_format param is not accepted by torch.ones
                           memory_format=memory_format, pin_memory=pin_memory,)
    elif tensor_init_params.create_op == CreateOp.ZEROS:
        return torch.zeros(*size,
                           dtype=dtype,
                           layout=layout,
                           device=local_device,
                           pin_memory=pin_memory,
                           requires_grad=requires_grad,)
    elif tensor_init_params.create_op == CreateOp.RAND:
        return torch.rand(*size,
                          dtype=dtype,
                          layout=layout,
                          device=local_device,
                          pin_memory=pin_memory,
                          requires_grad=requires_grad,)
    elif tensor_init_params.create_op == CreateOp.FULL:
        return torch.full(size=size,
                          fill_value=tensor_init_params.fill_value,
                          layout=layout,
                          dtype=dtype,
                          requires_grad=requires_grad,
                          device=local_device, )
    else:
        raise ValueError(f'Unsupported create_op: {tensor_init_params.create_op}')
