def full(sharding_spec: ShardingSpec,
         size,
         fill_value=torch.types.Number,
         dtype=None,
         layout=torch.strided,
         requires_grad=False,
         pin_memory=False,
         memory_format=torch.contiguous_format,
         process_group=None,
         init_rrefs=False):
    """
    Creates a :class:`ShardedTensor` filled with fill_value. The tensor’s dtype
        is inferred from fill_value. If dtype is specified, it will override the
        inferred type from fill_value. Needs to be called on all ranks in an SPMD fashion.

    Args:
        sharding_spec (:class:`torch.distributed._sharding_spec.ShardingSpec`): The specification
            describing how to shard the Tensor.
        size (int...):  a list, tuple, or `torch.Size` of integers defining the shape of the
            output tensor.
        fill_value (Scalar) – the value to fill the output tensor with.

    Keyword args:
        dtype (:class:`torch.dtype`, optional): the desired data type of returned tensor.
            Default: if ``None``, uses a global default (see :func:`torch.set_default_tensor_type`).
        layout (:class:`torch.layout`, optional): the desired layout of returned Tensor.
            Default: ``torch.strided``.
        requires_grad (bool, optional): If autograd should record operations on the
            returned tensor. Default: ``False``.
        pin_memory (bool, optional): If set, returned tensor would be allocated in
            the pinned memory. Works only for CPU tensors. Default: ``False``.
        process_group (ProcessGroup, optional): The process group to work on. If None,
            the default process group will be used.
        init_rrefs (bool, optional): Whether or not to initialize
            :class:`torch.distributed.rpc.RRef`s pointing to remote shards.
            Need to initialize the RPC Framework if specified as ``True``.
            Default: ``False``.

    Returns:
        A :class:`ShardedTensor` object on each rank
    """
    tensor_properties = TensorProperties(
        dtype=dtype, layout=layout, requires_grad=requires_grad,
        pin_memory=pin_memory, memory_format=memory_format,
    )
    tensor_init_params = TensorInitParams(
        create_op=CreateOp.FULL, fill_value=fill_value, tensor_properties=tensor_properties)
    return ShardedTensor(
        sharding_spec,
        *size,
        tensor_init_params=tensor_init_params,
        process_group=process_group,
        init_rrefs=init_rrefs,
    )
