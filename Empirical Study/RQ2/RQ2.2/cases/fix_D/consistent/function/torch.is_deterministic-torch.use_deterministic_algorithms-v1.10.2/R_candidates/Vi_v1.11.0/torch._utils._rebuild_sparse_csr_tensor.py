def _rebuild_sparse_csr_tensor(layout, data):
    if layout == torch.sparse_csr:
        crow_indices, col_indices, values, size = data
        result = torch._sparse_csr_tensor_unsafe(crow_indices, col_indices, values, size)
        _sparse_tensors_to_validate.append(result)
        return result

    raise NotImplementedError("rebuilding sparse tensor for layout %s" % (layout))
