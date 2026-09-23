def safe_is_leaf(t: Union[MetaTensorDesc, torch.Tensor]) -> bool:
    try:
        return t.is_leaf
    except RuntimeError:
        # inference mode can trigger this
        return False
