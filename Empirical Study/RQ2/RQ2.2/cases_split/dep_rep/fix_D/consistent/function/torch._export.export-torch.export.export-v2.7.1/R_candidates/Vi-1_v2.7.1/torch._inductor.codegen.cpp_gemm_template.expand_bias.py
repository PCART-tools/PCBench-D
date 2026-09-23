def expand_bias(B: Optional[_T], X: _T) -> Optional[_T]:
    """
    Expand Bias to the same size of X.
    """
    if B is not None:
        if isinstance(B, ir.IRNode):
            if not isinstance(B, ir.TensorBox):
                B = ir.TensorBox(B)
            assert hasattr(X, "get_size")
            B = L.expand(B, (X.get_size()[0], B.get_size()[-1]))
        else:
            assert isinstance(B, torch.Tensor)
            assert isinstance(X, torch.Tensor)
            B = B.expand(X.shape[0], B.shape[-1])
    return B
