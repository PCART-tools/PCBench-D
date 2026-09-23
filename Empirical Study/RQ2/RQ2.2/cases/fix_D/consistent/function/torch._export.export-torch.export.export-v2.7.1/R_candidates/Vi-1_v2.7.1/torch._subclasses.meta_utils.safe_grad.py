def safe_grad(t: _TensorLikeT) -> Optional[_TensorLikeT]:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", "The .grad attribute of a Tensor")
        return t.grad
