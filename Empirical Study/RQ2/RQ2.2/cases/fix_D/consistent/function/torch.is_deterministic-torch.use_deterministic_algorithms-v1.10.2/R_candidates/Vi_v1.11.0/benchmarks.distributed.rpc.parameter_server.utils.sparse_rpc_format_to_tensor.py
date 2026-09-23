def sparse_rpc_format_to_tensor(sparse_rpc_format):
    r"""
    A helper function creates a sparse_coo_tensor from indices, values, and size.
    Args:
        sparse_rpc_format (list): sparse_coo_tensor represented as a list
    """
    return torch.sparse_coo_tensor(
        sparse_rpc_format[0], sparse_rpc_format[1], sparse_rpc_format[2]
    ).coalesce()
