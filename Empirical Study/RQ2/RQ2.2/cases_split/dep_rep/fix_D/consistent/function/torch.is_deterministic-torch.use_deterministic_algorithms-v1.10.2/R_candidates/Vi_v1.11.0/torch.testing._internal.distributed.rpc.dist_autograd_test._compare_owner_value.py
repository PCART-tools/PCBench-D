def _compare_owner_value(context_id, rref, grad):
    grads = dist_autograd.get_gradients(context_id)
    x = grads[rref.local_value()]
    if x.is_sparse:
        assert grad.is_sparse
        x = x.to_dense()
        grad = grad.to_dense()
    else:
        assert not grad.is_sparse
    return torch.equal(x, grad)
