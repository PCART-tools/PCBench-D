def transpose_w(W: _T, trans_w: bool) -> _T:
    """
    Transpose W based on the trans_w flag.
    """
    if isinstance(W, ir.IRNode):
        if trans_w:
            if not isinstance(W, ir.TensorBox):
                W = ir.TensorBox(W)
            W = L.permute(W, [1, 0])
    else:
        if trans_w:
            assert isinstance(W, torch.Tensor)
            W = W.transpose(0, 1)
    return W
