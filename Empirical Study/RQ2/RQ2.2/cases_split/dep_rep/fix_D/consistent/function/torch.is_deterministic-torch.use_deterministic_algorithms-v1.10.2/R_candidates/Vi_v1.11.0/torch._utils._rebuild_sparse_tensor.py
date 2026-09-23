def _rebuild_sparse_tensor(layout, data):
    if layout == torch.sparse_coo:
        indices, values, size = data
        result = torch._sparse_coo_tensor_unsafe(indices, values, size)
        _sparse_tensors_to_validate.append(result)
        return result

    raise NotImplementedError("rebuilding sparse tensor for layout %s" % (layout))
