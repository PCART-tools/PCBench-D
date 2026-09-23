def _validate_loaded_sparse_tensors():
    try:
        for t in _sparse_tensors_to_validate:
            torch._validate_sparse_coo_tensor_args(t._indices(), t._values(),
                                                   t.size())
    finally:
        _sparse_tensors_to_validate.clear()
