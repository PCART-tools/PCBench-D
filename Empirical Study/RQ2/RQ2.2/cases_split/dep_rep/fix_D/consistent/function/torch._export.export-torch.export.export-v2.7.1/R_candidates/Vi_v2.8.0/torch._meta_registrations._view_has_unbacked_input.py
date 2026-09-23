def _view_has_unbacked_input(a, shape):
    from torch.fx.experimental.symbolic_shapes import has_hint

    return (
        any(not has_hint(s) for s in a.size())
        or any(not has_hint(s) for s in a.stride())
        or any(not has_hint(s) for s in shape)
    )
