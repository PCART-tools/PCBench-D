def _construct_standard_basis_for(tensors, tensor_numels):
    for basis in _chunked_standard_basis_for_(tensors, tensor_numels, chunk_size=None):
        return basis
