def _validate_loaded_sparse_tensors():
    try:
        for t in _sparse_tensors_to_validate:
            if t.is_sparse:
                torch._validate_sparse_coo_tensor_args(t._indices(), t._values(),
                                                       t.size())
            elif t.is_sparse_csr:
                # TODO: Validation currently involves an expensive traversal
                # on CPU, which may include a device transfer.
                torch._validate_sparse_csr_tensor_args(t.crow_indices(), t.col_indices(),
                                                       t.values(), t.size())
            else:
                raise NotImplementedError(
                    '_validate_loaded_sparse_tensors for layout `%s`' % (t.layout))

    finally:
        _sparse_tensors_to_validate.clear()
