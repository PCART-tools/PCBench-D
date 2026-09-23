def _construct_standard_basis_for(tensors: Tuple[torch.Tensor, ...], tensor_numels: Tuple[int, ...]) -> Tuple[torch.Tensor, ...]:
    # This function:
    # - constructs a N=sum(tensor_numels) standard basis. i.e. an NxN identity matrix.
    # - Splits the identity matrix into chunks with each chunk size determined by `tensor_numels`.
    # - Each chunk corresponds to one tensor. The chunk has the same dtype and
    #   device as the tensor
    #
    # For example, with tensor_numels = [1, 2, 1], this function returns:
    # ( tensor([[1],     tensor([[0, 0],      tensor([[0],
    #           [0],             [1, 0],              [0],
    #           [0],             [0, 1],              [0],
    #           [0]])  ,         [0, 0]])  ,          [1]])  )
    #
    # Precondition: tensor_numels == tuple(tensor.numel() for tensor in tensors)
    # Precondition: tensors always has at least one element.
    #
    # See NOTE: [Computing jacobian with vmap and grad for multiple tensors]
    # for context behind this function. All the pre-conditions are guarded for
    # in torch.autograd.functional.jacobian.
    assert len(tensors) == len(tensor_numels)
    assert len(tensors) > 0
    total_numel = sum(tensor_numels)
    diag_start_indices = (0, *torch.tensor(tensor_numels).cumsum(dim=0)[:-1].neg().unbind())
    chunks = tuple(tensor.new_zeros(total_numel, tensor_numel)
                   for tensor, tensor_numel in zip(tensors, tensor_numels))
    for chunk, diag_start_idx in zip(chunks, diag_start_indices):
        chunk.diagonal(diag_start_idx).fill_(1)
    return chunks
