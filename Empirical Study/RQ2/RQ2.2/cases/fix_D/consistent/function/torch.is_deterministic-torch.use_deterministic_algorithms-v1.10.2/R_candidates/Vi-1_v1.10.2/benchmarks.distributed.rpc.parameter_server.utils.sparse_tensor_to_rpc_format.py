def sparse_tensor_to_rpc_format(sparse_tensor):
    r"""
    A helper function creates a list containing the indices, values, and size
    of a coalesced sparse tensor.
    Args:
        sparse_tensor (torch.Tensor): sparse_coo_tensor represented as a list
    """
    sparse_tensor = sparse_tensor.coalesce()
    return [sparse_tensor.indices(), sparse_tensor.values(), sparse_tensor.size()]
