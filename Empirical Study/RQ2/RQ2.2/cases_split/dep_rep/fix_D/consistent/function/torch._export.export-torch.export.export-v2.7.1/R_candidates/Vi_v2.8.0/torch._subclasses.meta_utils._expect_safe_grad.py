def _expect_safe_grad(t: _TensorLikeT) -> _TensorLikeT:
    grad = safe_grad(t)
    assert grad is not None
    return grad
