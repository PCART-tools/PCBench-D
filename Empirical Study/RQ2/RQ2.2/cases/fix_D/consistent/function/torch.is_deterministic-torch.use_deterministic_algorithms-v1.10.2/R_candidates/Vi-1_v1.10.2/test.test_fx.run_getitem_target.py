def run_getitem_target():
    from torch.fx._symbolic_trace import _wrapped_methods_to_patch
    _wrapped_methods_to_patch.append((torch.Tensor, "__getitem__"))
    try:
        TestFX().getitem_inner()
    finally:
        _wrapped_methods_to_patch.pop()
